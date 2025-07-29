from typing import Dict, Any, List, Union, Optional, Tuple
from devops_ai.agents.base_agent import BaseAgent
import os
import json
import logging
import getpass
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import uuid
import yaml

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InfraSuggestAgent(BaseAgent):
    """Agent for providing infrastructure recommendations including AWS machine types and IAC generation"""
    
    def __init__(self):
        super().__init__()
        self.aws_credentials = None
        # Validate OpenAI API key on initialization
        self._validate_api_credentials()
        
    def _analyze_aws_instance_requirements(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze component requirements and suggest optimal AWS instance type"""
        prompt = f"""Based on the following component requirements, suggest the optimal AWS EC2 instance type:

Component: {component.get('component', 'Unknown')}
Description: {component.get('description', 'No description')}
CPU Cores: {component.get('cpu_cores', 'Not specified')}
Memory: {component.get('memory_gb', 'Not specified')} GB
Storage: {component.get('storage', 'Not specified')}
Networking: {component.get('networking', 'Not specified')}
Scaling: {component.get('scaling', 'Not specified')}

Please provide your recommendation in the following JSON format:
{{
    "instance_type": "Recommended EC2 instance type",
    "reasoning": "Explanation for the recommendation",
    "cost_estimate": "Estimated monthly cost",
    "performance_characteristics": {{
        "cpu": "CPU performance characteristics",
        "memory": "Memory performance characteristics",
        "network": "Network performance characteristics"
    }},
    "alternative_options": [
        {{
            "instance_type": "Alternative instance type",
            "pros": ["List of advantages"],
            "cons": ["List of disadvantages"]
        }}
    ]
}}
"""
        try:
            response = self.llm.invoke(prompt)
            response_text = response.content.strip()
            
            # Try to extract JSON from potentially markdown-wrapped response
            # Check if response is wrapped in markdown code blocks
            if "```json" in response_text:
                start_idx = response_text.find("```json") + 7
                end_idx = response_text.rfind("```")
                if end_idx > start_idx:
                    response_text = response_text[start_idx:end_idx].strip()
            elif response_text.startswith("```"):
                start_idx = response_text.find("```") + 3
                end_idx = response_text.rfind("```")
                if end_idx > start_idx:
                    response_text = response_text[start_idx:end_idx].strip()
            
            try:
                recommendation = json.loads(response_text)
                return recommendation
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON decode error: {json_err}. Raw response: {response_text[:100]}...")
                raise
                
        except Exception as e:
            logger.error(f"Error analyzing AWS instance requirements: {str(e)}")
            return {
                "instance_type": "t3.micro",
                "reasoning": "Fallback to t3.micro due to analysis error",
                "cost_estimate": "Unknown",
                "performance_characteristics": {
                    "cpu": "1 vCPU",
                    "memory": "1 GB",
                    "network": "Low to Moderate"
                },
                "alternative_options": []
            }

    def analyze(self, query: str = "", repo_path: str = None, generate_iac: bool = False, deploy: bool = False, iac_format: str = "cloudformation") -> str:
        """
        Get infrastructure recommendations based on repository context or user query.
        Optionally generate Infrastructure as Code (IAC) and deploy to AWS.

        Args:
            query: Optional natural language input for infrastructure suggestions
            repo_path: Path to local git repository for contextual analysis
            generate_iac: Whether to generate IAC templates (CloudFormation or Ansible)
            deploy: Whether to deploy the infrastructure to AWS
            iac_format: Format of IAC to generate ("cloudformation" or "ansible")

        Returns:
            str: Infrastructure recommendations in structured format
        """
        try:
            # Check if API credentials are valid before proceeding
            import os
            if not os.getenv("OPENAI_API_KEY"):
                logger.error("OPENAI_API_KEY environment variable is not set")
                return self._generate_fallback_response("API Error: OpenAI API key is not set")
                
            # Extract repository context if provided
            repo_context = ""
            repo_summary = {}

            if repo_path:
                try:
                    repo_data = self.analyze_repository(repo_path)
                    detected_services = self._detect_services_from_repo(repo_data)
                    repo_summary = {
                        "structure": repo_data.get("tree", {}),
                        "key_files": self._extract_key_file_contents(repo_path),
                        "services": detected_services
                    }

                    repo_context = self._format_repo_context_for_prompt(repo_summary)

                except Exception as e:
                    logger.warning(f"Failed to extract repository context: {str(e)}")

            # Build prompt for LLM
            prompt = f"""Based on the following context, provide detailed infrastructure recommendations for ONLY the detected components/services in the repository. 
DO NOT invent or assume components that are not explicitly mentioned in the detected services list.

{repo_context}

User Query: {query}

Please provide your response in the following JSON format, wrapped in triple backticks:
```json
{{
  "architecture_overview": "High-level architecture description based ONLY on the detected components",
  "infrastructure_recommendations": [
    {{
      "component": "Service/Component name (MUST match one of the detected components)",
      "description": "What this component does based on repository context",
      "cpu_cores": "Number of CPU cores needed",
      "memory_gb": "Memory (RAM) required in GB",
      "storage": "Storage requirements (e.g., '100GB SSD')",
      "networking": "Networking needs (e.g., public/private subnet)",
      "availability_zones": "Number of AZs recommended",
      "scaling": "Scaling strategy (e.g., auto-scaling group)"
    }}
  ],
  "resource_optimization": "Strategies for optimizing resources",
  "cost_saving_tips": "Tips to reduce cloud costs",
  "security_best_practices": "Security hardening recommendations",
  "deployment_pipeline_suggestions": "CI/CD pipeline recommendations"
}}
```
"""
            logger.info("Invoking LLM for infrastructure recommendation...")
            try:
                # Implement retry logic with exponential backoff
                max_retries = 3
                retry_count = 0
                last_error = None
                response_text = ""
                
                while retry_count < max_retries:
                    try:
                        response = self.llm.invoke(prompt)
                        response_text = response.content.strip()
                        break  # Success, exit the retry loop
                    except Exception as e:
                        last_error = e
                        retry_count += 1
                        logger.warning(f"LLM API call failed (attempt {retry_count}/{max_retries}): {str(e)}")
                        
                        if retry_count < max_retries:
                            # Exponential backoff: wait longer between each retry
                            import time
                            wait_time = 2 ** retry_count  # 2, 4, 8 seconds
                            logger.info(f"Retrying in {wait_time} seconds...")
                            time.sleep(wait_time)
                
                if retry_count == max_retries:
                    logger.error(f"Failed to invoke LLM after {max_retries} attempts")
                    return self._generate_fallback_response(f"API Error: Unable to connect to LLM service after {max_retries} attempts")
            except Exception as api_error:
                logger.error(f"API error: {str(api_error)}")
                # Generate a fallback response without using the API
                return self._generate_fallback_response(f"API Error: {str(api_error)}")

            # Try to extract JSON from markdown
            json_response = self._extract_json(response_text)

            if not json_response:
                # Create a fallback response if JSON parsing fails
                json_response = {
                    "architecture_overview": "Unable to parse structured response. Raw output:",
                    "infrastructure_recommendations": [
                        {
                            "component": "General Infrastructure",
                            "description": response_text[:500] + ("..." if len(response_text) > 500 else ""),
                            "cpu_cores": "Not specified",
                            "memory_gb": "Not specified",
                            "storage": "Not specified",
                            "networking": "Not specified",
                            "availability_zones": "Not specified",
                            "scaling": "Not specified"
                        }
                    ],
                    "resource_optimization": "See raw output",
                    "cost_saving_tips": "See raw output",
                    "security_best_practices": "See raw output",
                    "deployment_pipeline_suggestions": "See raw output"
                }

            # Analyze AWS instance requirements for each component
            for comp in json_response.get("infrastructure_recommendations", []):
                instance_analysis = self._analyze_aws_instance_requirements(comp)
                comp["aws_ec2_instance_type"] = instance_analysis["instance_type"]
                comp["instance_analysis"] = instance_analysis

            # Write report or logs if needed
            self._save_infra_recommendation_report(repo_path, json_response)
            
            # Generate IAC if requested
            iac_output = ""
            if generate_iac:
                try:
                    if iac_format.lower() == "ansible":
                        iac_templates = self._generate_ansible_playbooks(json_response)
                        self._save_ansible_playbooks(repo_path, iac_templates)
                        iac_output = "\n\n=== INFRASTRUCTURE AS CODE GENERATED ===\n"
                        iac_output += f"Ansible playbooks have been generated in {repo_path}/ansible/\n"
                    else:  # Default to CloudFormation
                        iac_templates = self._generate_cloudformation_templates(json_response)
                        self._save_cloudformation_templates(repo_path, iac_templates)
                        iac_output = "\n\n=== INFRASTRUCTURE AS CODE GENERATED ===\n"
                        iac_output += f"CloudFormation templates have been generated in {repo_path}/cloudformation/\n"
                except Exception as e:
                    logger.error(f"Error generating IAC: {str(e)}", exc_info=True)
                    iac_output = f"\n\nError generating Infrastructure as Code: {str(e)}"
            
            # Deploy to AWS if requested
            deployment_output = ""
            if deploy:
                if not self.aws_credentials:
                    self._collect_aws_credentials()
                
                if self.aws_credentials:
                    try:
                        if iac_format.lower() == "ansible":
                            deployment_result = self._deploy_with_ansible(repo_path, json_response)
                        else:
                            deployment_result = self._deploy_to_aws(repo_path, json_response)
                        deployment_output = "\n\n=== DEPLOYMENT STATUS ===\n"
                        deployment_output += deployment_result
                    except Exception as e:
                        logger.error(f"Error deploying to AWS: {str(e)}", exc_info=True)
                        deployment_output = f"\n\nError deploying to AWS: {str(e)}"
                else:
                    deployment_output = "\n\nAWS deployment skipped: No credentials provided."

            # Return formatted output
            return self._format_output(json_response) + iac_output + deployment_output

        except Exception as e:
            logger.error(f"Error generating infrastructure suggestion: {str(e)}", exc_info=True)
            return f"Error generating infrastructure suggestions: {str(e)}"

    def _extract_key_file_contents(self, repo_path: str, max_files: int = 5, max_chars: int = 2000) -> Dict[str, str]:
        """Extract content from key files for LLM context"""
        key_files = []
        for root, _, files in os.walk(repo_path):
            for fname in files:
                if fname.lower() in {"package.json", "requirements.txt", "Dockerfile", "docker-compose.yml",
                                     "pom.xml", "build.gradle", "setup.py", "Gemfile", ".gitignore"}:
                    key_files.append(os.path.relpath(os.path.join(root, fname), repo_path))

        file_contents = {}
        for fname in key_files[:max_files]:
            fpath = os.path.join(repo_path, fname)
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()[:max_chars]
                        file_contents[fname] = content
                except Exception as e:
                    file_contents[fname] = f"[ERROR reading file: {e}]"
        return file_contents

    def _detect_services_from_repo(self, repo_data: dict) -> List[Dict[str, Any]]:
        """Try to detect services/components from repository structure with detailed information"""
        services = []
        service_names = set()
        
        # Get repository tree
        tree = repo_data.get("tree", {})
        
        # 1. Detect services from Dockerfiles
        for path in tree.keys():
            if "dockerfile" in path.lower() or path.lower().endswith(".dockerfile"):
                # Extract service name from Dockerfile.service_name pattern
                parts = os.path.basename(path).split('.')
                if len(parts) > 1 and parts[0].lower() == "dockerfile":
                    service_name = parts[1].lower()
                    if service_name not in service_names:
                        service_names.add(service_name)
                        services.append({
                            "component": service_name,
                            "description": f"Service identified from {path}",
                            "source": "dockerfile"
                        })
        
        # 2. Detect services from docker-compose.yml
        docker_compose_paths = [p for p in tree.keys() if p.lower().endswith("docker-compose.yml")]
        for dc_path in docker_compose_paths:
            try:
                # Try to read docker-compose.yml content from repo_data or file system
                dc_content = None
                if "content" in repo_data and dc_path in repo_data["content"]:
                    dc_content = repo_data["content"][dc_path]
                else:
                    # Attempt to read from file system if available
                    full_path = os.path.join(os.path.dirname(dc_path), "docker-compose.yml")
                    if os.path.exists(full_path):
                        with open(full_path, 'r') as f:
                            dc_content = f.read()
                
                if dc_content:
                    # Parse YAML content
                    try:
                        dc_yaml = yaml.safe_load(dc_content)
                        if dc_yaml and "services" in dc_yaml:
                            for svc_name, svc_config in dc_yaml["services"].items():
                                if svc_name not in service_names:
                                    service_names.add(svc_name)
                                    # Extract more details if available
                                    description = f"Service defined in docker-compose.yml"
                                    if "image" in svc_config:
                                        description += f", using image {svc_config['image']}"
                                    
                                    services.append({
                                        "component": svc_name,
                                        "description": description,
                                        "source": "docker-compose"
                                    })
                    except Exception as e:
                        logger.warning(f"Error parsing docker-compose.yml: {str(e)}")
            except Exception as e:
                logger.warning(f"Error processing docker-compose file {dc_path}: {str(e)}")
        
        # 3. Detect services from common project structures
        service_dirs = set()
        service_keywords = ["api", "web", "service", "worker", "db", "database", "cache", "gateway", "auth", "frontend", "backend"]
        
        for path in tree.keys():
            parts = path.split("/")
            if len(parts) > 1:
                # Check if first directory component is a service keyword
                if parts[0].lower() in service_keywords and parts[0] not in service_names:
                    service_dirs.add(parts[0])
        
        # Add services from directory structure
        for svc_dir in service_dirs:
            if svc_dir not in service_names:
                service_names.add(svc_dir)
                services.append({
                    "component": svc_dir,
                    "description": f"Service identified from directory structure",
                    "source": "directory"
                })
        
        # 4. If no services detected, add default components based on repository type
        if not services:
            # Check for common application types
            has_frontend = any("index.html" in p.lower() for p in tree.keys())
            has_backend = any(p.lower().endswith((".py", ".js", ".java", ".go")) for p in tree.keys())
            
            if has_frontend:
                services.append({
                    "component": "frontend",
                    "description": "Frontend web application detected from repository structure",
                    "source": "inferred"
                })
            
            if has_backend:
                services.append({
                    "component": "backend",
                    "description": "Backend application detected from repository structure",
                    "source": "inferred"
                })
            
            # If still no services detected, add a generic application component
            if not services:
                services.append({
                    "component": "application",
                    "description": "Generic application component",
                    "source": "default"
                })
        
        return services

    def _format_repo_context_for_prompt(self, repo_summary: dict) -> str:
        """Format repository data into a prompt-friendly string"""
        context = "\nRepository Context:\n"

        if "structure" in repo_summary:
            context += "\nDirectory Tree:\n"
            for path in repo_summary["structure"]:
                context += f"- {path}\n"

        if "key_files" in repo_summary:
            context += "\nKey Files Content:\n"
            for fname, content in repo_summary["key_files"].items():
                context += f"\n--- {fname} ---\n{content[:500]}...\n"

        if "services" in repo_summary and repo_summary["services"]:
            context += "\nDetected Services/Components:\n"
            for svc in repo_summary["services"]:
                component = svc.get("component", "Unknown")
                description = svc.get("description", "No description")
                source = svc.get("source", "Unknown")
                context += f"- {component}: {description} (Source: {source})\n"

        return context

    def _extract_json(self, text: str) -> Union[Dict, None]:
        """Extract JSON from potentially markdown-wrapped response"""
        # Try to extract JSON from markdown code block
        start_idx = text.find("```json")
        if start_idx != -1:
            end_idx = text.rfind("```")
            if end_idx > start_idx:
                json_str = text[start_idx + 7:end_idx].strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error in code block: {e}")
                    # Don't return None yet, try other methods
        
        # Try to extract JSON without markdown wrapper
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # If all JSON parsing fails, create a fallback JSON structure
            logger.warning("Failed to parse JSON from LLM response, using fallback structure")
            
            # Create a fallback structure with the raw text
            return {
                "architecture_overview": "Unable to parse structured response. Raw output:",
                "infrastructure_recommendations": [
                    {
                        "component": "General Infrastructure",
                        "description": text[:500] + ("..." if len(text) > 500 else ""),
                        "aws_ec2_instance_type": "Not specified",
                        "cpu_cores": "Not specified",
                        "memory_gb": "Not specified",
                        "storage": "Not specified",
                        "networking": "Not specified",
                        "availability_zones": "Not specified",
                        "scaling": "Not specified"
                    }
                ],
                "resource_optimization": "See raw output",
                "cost_saving_tips": "See raw output",
                "security_best_practices": "See raw output",
                "deployment_pipeline_suggestions": "See raw output"
            }

    def _save_infra_recommendation_report(self, repo_path: str, report: dict):
        """Save infrastructure recommendation as JSON file"""
        if repo_path and os.path.isdir(repo_path):
            report_path = os.path.join(repo_path, "infrastructure_recommendation.json")
            try:
                with open(report_path, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2)
                logger.info(f"Saved infrastructure report to {report_path}")
            except Exception as e:
                logger.warning(f"Failed to save infrastructure report: {str(e)}")

    def _validate_api_credentials(self):
        """Validate OpenAI API key and other credentials"""
        import os
        from openai import OpenAI
        
        # Check if OpenAI API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY environment variable is not set")
            return False
            
        # Try a simple API call to validate the key
        try:
            # Create a minimal client for validation only
            client = OpenAI(api_key=api_key)
            # Make a minimal API call to check if the key is valid
            models = client.models.list()  # Remove the limit parameter
            logger.info("OpenAI API credentials validated successfully")
            return True
        except Exception as e:
            logger.warning(f"OpenAI API key validation failed: {str(e)}")
            return False
    
    def _generate_fallback_response(self, error_message: str) -> str:
        """Generate a fallback response when LLM API call fails"""
        # Create a basic fallback response with error information
        fallback_json = {
            "architecture_overview": f"Unable to generate detailed recommendations due to API error: {error_message}. Using fallback recommendations.",
            "infrastructure_recommendations": [
                {
                    "component": "Web Application",
                    "description": "Basic web application service",
                    "aws_ec2_instance_type": "t3.medium",
                    "cpu_cores": "2",
                    "memory_gb": "4",
                    "storage": "20GB SSD",
                    "networking": "Public subnet with security group",
                    "availability_zones": "2",
                    "scaling": "Auto-scaling group with 2-4 instances"
                },
                {
                    "component": "Database",
                    "description": "Relational database for application data",
                    "aws_ec2_instance_type": "t3.large",
                    "cpu_cores": "2",
                    "memory_gb": "8",
                    "storage": "100GB SSD",
                    "networking": "Private subnet",
                    "availability_zones": "2",
                    "scaling": "Multi-AZ deployment"
                }
            ],
            "resource_optimization": "Use reserved instances for predictable workloads. Implement auto-scaling for variable loads.",
            "cost_saving_tips": "Consider using Spot instances for non-critical workloads. Implement lifecycle policies for EBS volumes.",
            "security_best_practices": "Use security groups to restrict access. Enable encryption for data at rest and in transit.",
            "deployment_pipeline_suggestions": "Implement CI/CD pipeline with AWS CodePipeline or GitHub Actions."
        }
        
        # Format and return the fallback response
        return self._format_output(fallback_json)

    def _format_output(self, result: dict) -> str:
        """Format final output for user readability"""
        output = ""

        output += "=== INFRASTRUCTURE RECOMMENDATION ===\n\n"
        output += "Architecture Overview:\n"
        output += result.get("architecture_overview", "") + "\n\n"

        output += "Infrastructure Components:\n"
        for comp in result.get("infrastructure_recommendations", []):
            output += f"- {comp['component']} ({comp['aws_ec2_instance_type']}):\n"
            output += f"  Description: {comp['description']}\n"
            output += f"  CPU: {comp['cpu_cores']} cores, Memory: {comp['memory_gb']} GB\n"
            output += f"  Storage: {comp['storage']}\n"
            output += f"  Networking: {comp['networking']}\n"
            output += f"  Scaling: {comp['scaling']}\n\n"

        output += "Resource Optimization:\n"
        output += result.get("resource_optimization", "") + "\n\n"

        output += "Cost Saving Tips:\n"
        output += result.get("cost_saving_tips", "") + "\n\n"

        output += "Security Best Practices:\n"
        output += result.get("security_best_practices", "") + "\n\n"

        output += "Deployment Pipeline Suggestions:\n"
        output += result.get("deployment_pipeline_suggestions", "")

        return output
        
    def _generate_cloudformation_templates(self, infra_recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate CloudFormation templates based on infrastructure recommendations using LLM"""
        templates = {}
        
        # Extract key information from recommendations
        components = infra_recommendations.get("infrastructure_recommendations", [])
        architecture_overview = infra_recommendations.get("architecture_overview", "")
        
        # Build prompt for LLM to generate CloudFormation template
        prompt = f"""Generate a complete AWS CloudFormation template based on the following infrastructure requirements.

Architecture Overview:
{architecture_overview}

Infrastructure Components:
"""

        # Add each component's details to the prompt
        for comp in components:
            prompt += f"""
- Component: {comp.get('component', 'Unknown')}
  Description: {comp.get('description', 'No description')}
  EC2 Instance Type: {comp.get('aws_ec2_instance_type', 't3.micro')}
  CPU: {comp.get('cpu_cores', 'Not specified')} cores
  Memory: {comp.get('memory_gb', 'Not specified')} GB
  Storage: {comp.get('storage', 'Not specified')}
  Networking: {comp.get('networking', 'Not specified')}
  Availability Zones: {comp.get('availability_zones', 'Not specified')}
  Scaling Strategy: {comp.get('scaling', 'Not specified')}
"""
        
        # Add instructions for generating the CloudFormation template
        prompt += """

Please generate a complete AWS CloudFormation template in JSON format that implements this infrastructure.
The template should include:
1. Appropriate VPC and networking resources
2. Security groups with proper ingress/egress rules
3. EC2 instances or Auto Scaling Groups as specified
4. Any necessary IAM roles and policies
5. Appropriate resource tagging
6. Outputs for important resource IDs

The template should follow AWS best practices and be optimized for security, reliability, and cost-efficiency.
Provide ONLY the CloudFormation template JSON without any explanations or markdown formatting.
"""

        logger.info("Invoking LLM to generate CloudFormation template...")
        try:
            # Invoke LLM to generate the CloudFormation template
            response = self.llm.invoke(prompt)
            template_text = response.content.strip()
            
            # Try to parse the response as JSON
            try:
                # Extract JSON if it's wrapped in code blocks
                if template_text.startswith("```") and template_text.endswith("```"):
                    # Extract content between code blocks
                    start_idx = template_text.find("\n") + 1
                    end_idx = template_text.rfind("```")
                    template_text = template_text[start_idx:end_idx].strip()
                
                # Validate the template is valid JSON
                json.loads(template_text)
                
                # Store the main template
                templates["main-stack.json"] = template_text
                
                # Generate component-specific templates if there are multiple components
                if len(components) > 1:
                    for idx, comp in enumerate(components):
                        component_name = comp["component"].replace(" ", "")
                        component_prompt = f"""Generate a CloudFormation template for just the {comp['component']} component with these specifications:
                        
- Description: {comp.get('description', 'No description')}
- EC2 Instance Type: {comp.get('aws_ec2_instance_type', 't3.micro')}
- CPU: {comp.get('cpu_cores', 'Not specified')} cores
- Memory: {comp.get('memory_gb', 'Not specified')} GB
- Storage: {comp.get('storage', 'Not specified')}
- Networking: {comp.get('networking', 'Not specified')}
- Availability Zones: {comp.get('availability_zones', 'Not specified')}
- Scaling Strategy: {comp.get('scaling', 'Not specified')}

Provide ONLY the CloudFormation template JSON without any explanations or markdown formatting.
"""
                        
                        # Only generate component templates for the first few components to avoid excessive API calls
                        if idx < 3:  # Limit to 3 component-specific templates
                            component_response = self.llm.invoke(component_prompt)
                            component_template = component_response.content.strip()
                            
                            # Extract JSON if wrapped in code blocks
                            if component_template.startswith("```") and component_template.endswith("```"):
                                start_idx = component_template.find("\n") + 1
                                end_idx = component_template.rfind("```")
                                component_template = component_template[start_idx:end_idx].strip()
                            
                            # Validate and store component template
                            try:
                                json.loads(component_template)
                                templates[f"{component_name.lower()}-stack.json"] = component_template
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse component template for {component_name} as JSON")
            
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse CloudFormation template as JSON: {str(e)}")
                # Create a fallback template if parsing fails
                fallback_template = self._create_fallback_template(infra_recommendations)
                templates["main-stack.json"] = json.dumps(fallback_template, indent=2)
        
        except Exception as e:
            logger.error(f"Error generating CloudFormation template with LLM: {str(e)}")
            # Create a fallback template if LLM invocation fails
            fallback_template = self._create_fallback_template(infra_recommendations)
            templates["main-stack.json"] = json.dumps(fallback_template, indent=2)
        
        return templates
        
    def _create_fallback_template(self, infra_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fallback CloudFormation template if LLM generation fails"""
        # Basic template structure
        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "Fallback CloudFormation template generated from infrastructure recommendations",
            "Parameters": {
                "EnvironmentName": {
                    "Description": "Environment name (e.g., dev, test, prod)",
                    "Type": "String",
                    "Default": "dev"
                },
                "VpcCIDR": {
                    "Description": "CIDR block for the VPC",
                    "Type": "String",
                    "Default": "10.0.0.0/16"
                }
            },
            "Resources": {
                "VPC": {
                    "Type": "AWS::EC2::VPC",
                    "Properties": {
                        "CidrBlock": {"Ref": "VpcCIDR"},
                        "EnableDnsSupport": True,
                        "EnableDnsHostnames": True,
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${EnvironmentName}-vpc"}}]
                    }
                },
                "PublicSubnet1": {
                    "Type": "AWS::EC2::Subnet",
                    "Properties": {
                        "VpcId": {"Ref": "VPC"},
                        "CidrBlock": {"Fn::Select": [0, {"Fn::Cidr": [{"Ref": "VpcCIDR"}, 4, 8]}]},
                        "AvailabilityZone": {"Fn::Select": [0, {"Fn::GetAZs": ""}]},
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${EnvironmentName}-public-subnet-1"}}]
                    }
                }
            },
            "Outputs": {
                "VpcId": {
                    "Description": "VPC ID",
                    "Value": {"Ref": "VPC"},
                    "Export": {"Name": {"Fn::Sub": "${EnvironmentName}-VpcId"}}
                }
            }
        }
        
        # Add resources for each component in the recommendations
        for idx, comp in enumerate(infra_recommendations.get("infrastructure_recommendations", [])):
            component_name = comp["component"].replace(" ", "")
            instance_type = comp["aws_ec2_instance_type"]
            
            # Add security group for the component
            sg_name = f"{component_name}SecurityGroup"
            template["Resources"][sg_name] = {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupDescription": f"Security group for {comp['component']}",
                    "VpcId": {"Ref": "VPC"},
                    "SecurityGroupIngress": [
                        {"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "CidrIp": "0.0.0.0/0"}
                    ],
                    "Tags": [{"Key": "Name", "Value": {"Fn::Sub": f"${{EnvironmentName}}-{component_name}-sg"}}]
                }
            }
            
            # Add EC2 instance or Auto Scaling Group based on scaling strategy
            if "auto" in comp.get("scaling", "").lower():
                # Create Launch Template
                lt_name = f"{component_name}LaunchTemplate"
                template["Resources"][lt_name] = {
                    "Type": "AWS::EC2::LaunchTemplate",
                    "Properties": {
                        "LaunchTemplateName": {"Fn::Sub": f"${{EnvironmentName}}-{component_name}-lt"},
                        "VersionDescription": "Initial version",
                        "LaunchTemplateData": {
                            "InstanceType": instance_type,
                            "SecurityGroupIds": [{"Ref": sg_name}],
                            "ImageId": "ami-0c55b159cbfafe1f0",
                            "UserData": {"Fn::Base64": {"Fn::Sub": f"#!/bin/bash\necho 'Setting up {comp['component']}'\n"}}
                        }
                    }
                }
                
                # Create Auto Scaling Group
                asg_name = f"{component_name}ASG"
                template["Resources"][asg_name] = {
                    "Type": "AWS::AutoScaling::AutoScalingGroup",
                    "Properties": {
                        "AutoScalingGroupName": {"Fn::Sub": f"${{EnvironmentName}}-{component_name}-asg"},
                        "LaunchTemplate": {
                            "LaunchTemplateId": {"Ref": lt_name},
                            "Version": {"Fn::GetAtt": [lt_name, "LatestVersionNumber"]}
                        },
                        "MinSize": 1,
                        "MaxSize": 3,
                        "DesiredCapacity": 2,
                        "VPCZoneIdentifier": [{"Ref": "PublicSubnet1"}],
                        "Tags": [{
                            "Key": "Name",
                            "Value": {"Fn::Sub": f"${{EnvironmentName}}-{component_name}"},
                            "PropagateAtLaunch": True
                        }]
                    }
                }
            else:
                # Create EC2 instance
                ec2_name = f"{component_name}Instance"
                template["Resources"][ec2_name] = {
                    "Type": "AWS::EC2::Instance",
                    "Properties": {
                        "InstanceType": instance_type,
                        "SecurityGroupIds": [{"Ref": sg_name}],
                        "SubnetId": {"Ref": "PublicSubnet1"},
                        "ImageId": "ami-0c55b159cbfafe1f0",
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": f"${{EnvironmentName}}-{component_name}"}}]
                    }
                }
        
        return template
    
    def _save_cloudformation_templates(self, repo_path: str, templates: Dict[str, str]) -> None:
        """Save CloudFormation templates to the repository"""
        if not repo_path or not os.path.isdir(repo_path):
            logger.warning("No valid repository path provided for saving CloudFormation templates")
            return
            
        # Create cloudformation directory if it doesn't exist
        cf_dir = os.path.join(repo_path, "cloudformation")
        os.makedirs(cf_dir, exist_ok=True)
        
        # Save each template
        for template_name, content in templates.items():
            template_path = os.path.join(cf_dir, template_name)
            try:
                with open(template_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"Saved CloudFormation template to {template_path}")
            except Exception as e:
                logger.warning(f"Failed to save CloudFormation template {template_name}: {str(e)}")
    
    def _collect_aws_credentials(self) -> None:
        """Securely collect AWS credentials from the user"""
        print("\n=== AWS Credentials Required for Deployment ===")
        print("Please enter your AWS credentials. These will only be used for this deployment and won't be stored permanently.")
        print("Note: For security, your input will not be displayed as you type.\n")
        
        try:
            aws_access_key = getpass.getpass("AWS Access Key ID: ")
            aws_secret_key = getpass.getpass("AWS Secret Access Key: ")
            aws_region = input("AWS Region (e.g., us-east-1): ")
            
            # Validate credentials
            if not aws_access_key or not aws_secret_key or not aws_region:
                print("Error: All credential fields are required.")
                return
            
            # Store credentials temporarily
            self.aws_credentials = {
                "aws_access_key_id": aws_access_key,
                "aws_secret_access_key": aws_secret_key,
                "region_name": aws_region
            }
            
            # Verify credentials
            try:
                session = boto3.Session(
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=aws_region
                )
                sts = session.client('sts')
                sts.get_caller_identity()
                print("AWS credentials verified successfully.")
            except Exception as e:
                print(f"Error verifying AWS credentials: {str(e)}")
                self.aws_credentials = None
                
        except KeyboardInterrupt:
            print("\nAWS credential collection cancelled.")
            self.aws_credentials = None
        except Exception as e:
            print(f"\nError collecting AWS credentials: {str(e)}")
            self.aws_credentials = None
    
    def _deploy_to_aws(self, repo_path: str, infra_recommendations: Dict[str, Any]) -> str:
        """Deploy infrastructure to AWS using CloudFormation"""
        if not self.aws_credentials:
            return "Error: AWS credentials not available. Please provide credentials first."
        
        # Create CloudFormation client
        try:
            cf_client = boto3.client(
                'cloudformation',
                aws_access_key_id=self.aws_credentials["aws_access_key_id"],
                aws_secret_access_key=self.aws_credentials["aws_secret_access_key"],
                region_name=self.aws_credentials["region_name"]
            )
            
            # Generate stack name
            stack_name = f"infra-{uuid.uuid4().hex[:8]}"
            
            # Get template path
            cf_dir = os.path.join(repo_path, "cloudformation")
            template_path = os.path.join(cf_dir, "main-stack.json")
            
            if not os.path.exists(template_path):
                # Generate templates if they don't exist
                templates = self._generate_cloudformation_templates(infra_recommendations)
                self._save_cloudformation_templates(repo_path, templates)
            
            # Read template content
            with open(template_path, "r") as f:
                template_body = f.read()
            
            # Create CloudFormation stack
            response = cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=[
                    {
                        'ParameterKey': 'EnvironmentName',
                        'ParameterValue': 'dev'
                    }
                ],
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
                OnFailure='ROLLBACK'
            )
            
            stack_id = response['StackId']
            return f"Deployment initiated successfully!\nStack Name: {stack_name}\nStack ID: {stack_id}\n\nYou can monitor the deployment status in the AWS CloudFormation console."
            
        except ClientError as e:
            logger.error(f"AWS CloudFormation error: {str(e)}", exc_info=True)
            return f"AWS CloudFormation error: {str(e)}"
        except NoCredentialsError:
            return "Error: AWS credentials not found or invalid."
        except Exception as e:
            logger.error(f"Deployment error: {str(e)}", exc_info=True)
            return f"Deployment error: {str(e)}"

    def _generate_ansible_playbooks(self, infra_recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate Ansible playbooks based on infrastructure recommendations using LLM"""
        # Extract key information from recommendations
        components = infra_recommendations.get("infrastructure_recommendations", [])
        architecture_overview = infra_recommendations.get("architecture_overview", "")
        
        # Build prompt for LLM to generate Ansible playbooks
        prompt = f"""Generate complete Ansible playbooks based on the following infrastructure requirements.

Architecture Overview:
{architecture_overview}

Infrastructure Components:
"""

        # Add each component's details to the prompt
        for comp in components:
            prompt += f"""
- Component: {comp.get('component', 'Unknown')}
  Description: {comp.get('description', 'No description')}
  EC2 Instance Type: {comp.get('aws_ec2_instance_type', 't3.micro')}
  CPU: {comp.get('cpu_cores', 'Not specified')} cores
  Memory: {comp.get('memory_gb', 'Not specified')} GB
  Storage: {comp.get('storage', 'Not specified')}
  Networking: {comp.get('networking', 'Not specified')}
  Availability Zones: {comp.get('availability_zones', 'Not specified')}
  Scaling Strategy: {comp.get('scaling', 'Not specified')}
"""
        
        # Add instructions for generating the Ansible playbooks
        prompt += """

Please generate the following Ansible playbooks in YAML format:

1. A main playbook (main.yml) that includes all component roles
2. Individual component playbooks for each infrastructure component
3. An inventory file (inventory.yml) that defines the hosts and groups

The playbooks should include:
- Appropriate tasks for provisioning and configuring each component
- Variables for customization
- Handlers for service management
- Tags for selective execution
- Proper error handling and idempotence
- Security best practices

Provide the playbooks in the following format:
```yaml
# [filename.yml]
# Playbook content here
```

For example:
```yaml
# main.yml
- name: Deploy Infrastructure
  hosts: all
  become: true
  roles:
    - webserver
    - database
```

Ensure the playbooks follow Ansible best practices and are optimized for AWS deployment.
"""

        logger.info("Invoking LLM to generate Ansible playbooks...")
        try:
            # Invoke LLM to generate the Ansible playbooks
            response = self.llm.invoke(prompt)
            playbooks_text = response.content.strip()
            
            # Parse the response to extract individual playbooks
            playbook_sections = self._extract_playbooks_from_response(playbooks_text)
            
            if not playbook_sections:
                logger.warning("Failed to extract playbooks from LLM response, using fallback")
                return self._generate_fallback_ansible_playbooks(infra_recommendations)
            
            return playbook_sections
            
        except Exception as e:
            logger.error(f"Error generating Ansible playbooks with LLM: {str(e)}")
            # Create fallback playbooks if LLM invocation fails
            return self._generate_fallback_ansible_playbooks(infra_recommendations)
    
    def _extract_playbooks_from_response(self, response_text: str) -> Dict[str, str]:
        """Extract individual playbooks from LLM response"""
        playbooks = {}
        
        # Look for playbook sections in the format: ```yaml\n# [filename.yml]\n...
        import re
        pattern = r'```(?:yaml)?\s*#\s*\[?([\w\.-]+\.yml)\]?\s*([\s\S]*?)```'
        matches = re.findall(pattern, response_text)
        
        if not matches:
            # Try alternative pattern without the filename in brackets
            pattern = r'```(?:yaml)?\s*#\s*([\w\.-]+\.yml)\s*([\s\S]*?)```'
            matches = re.findall(pattern, response_text)
        
        if not matches:
            # Try another pattern with just the filename as a comment
            pattern = r'```(?:yaml)?\s*([\w\.-]+\.yml)\s*([\s\S]*?)```'
            matches = re.findall(pattern, response_text)
            
        if not matches:
            # Last attempt: look for sections with clear filename headers but without code blocks
            pattern = r'# ([\w\.-]+\.yml)\s*([\s\S]*?)(?=# [\w\.-]+\.yml|$)'
            matches = re.findall(pattern, response_text)
        
        for filename, content in matches:
            # Clean up the content
            clean_content = content.strip()
            # Remove the filename if it appears at the beginning of the content
            if clean_content.startswith(filename):
                clean_content = clean_content[len(filename):].strip()
            
            playbooks[filename.strip()] = clean_content
        
        # If we couldn't extract any playbooks with the patterns, try to parse the whole response
        if not playbooks and '---' in response_text:
            # This might be a single YAML document, try to use it as main.yml
            playbooks['main.yml'] = response_text
        
        return playbooks
    
    def _generate_fallback_ansible_playbooks(self, infra_recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate fallback Ansible playbooks if LLM generation fails"""
        playbooks = {}
        
        # Generate main playbook
        main_playbook = {
            "name": "Infrastructure Deployment",
            "hosts": "all",
            "become": True,
            "vars": {
                "environment": "{{ env | default('dev') }}",
                "region": "{{ aws_region | default('us-east-1') }}"
            },
            "pre_tasks": [
                {
                    "name": "Update apt cache",
                    "apt": {
                        "update_cache": "yes",
                        "cache_valid_time": 3600
                    },
                    "when": "ansible_os_family == 'Debian'"
                }
            ],
            "roles": []
        }
        
        # Generate component-specific playbooks
        for comp in infra_recommendations.get("infrastructure_recommendations", []):
            component_name = comp["component"].replace(" ", "").lower()
            
            # Add role to main playbook
            main_playbook["roles"].append(component_name)
            
            # Generate component-specific playbook
            component_playbook = {
                "name": f"Deploy {comp['component']}",
                "hosts": component_name,
                "become": True,
                "vars": {
                    "instance_type": comp.get("aws_ec2_instance_type", "t3.micro"),
                    "cpu_cores": comp.get("cpu_cores", "1"),
                    "memory_gb": comp.get("memory_gb", "1"),
                    "storage": comp.get("storage", "20GB"),
                    "scaling": comp.get("scaling", "single")
                },
                "tasks": [
                    {
                        "name": "Install required packages",
                        "package": {
                            "name": "{{ item }}",
                            "state": "present"
                        },
                        "loop": [
                            "python3",
                            "python3-pip",
                            "git",
                            "docker.io"
                        ]
                    },
                    {
                        "name": "Configure system resources",
                        "block": [
                            {
                                "name": "Set CPU governor",
                                "command": "echo performance > /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor",
                                "when": "ansible_os_family == 'Linux'"
                            },
                            {
                                "name": "Configure swap space",
                                "command": "dd if=/dev/zero of=/swapfile bs=1M count={{ memory_gb * 1024 }} && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile",
                                "when": "ansible_os_family == 'Linux'"
                            }
                        ]
                    },
                    {
                        "name": "Setup application directory",
                        "file": {
                            "path": "/opt/{{ component_name }}",
                            "state": "directory",
                            "mode": "0755"
                        }
                    }
                ]
            }
            
            # Add scaling configuration if needed
            if "auto" in comp.get("scaling", "").lower():
                component_playbook["tasks"].extend([
                    {
                        "name": "Install AWS CLI",
                        "pip": {
                            "name": "awscli",
                            "state": "present"
                        }
                    },
                    {
                        "name": "Configure auto-scaling",
                        "template": {
                            "src": "templates/autoscaling.conf.j2",
                            "dest": "/etc/{{ component_name }}/autoscaling.conf",
                            "mode": "0644"
                        }
                    }
                ])
            
            # Store component playbook
            playbooks[f"{component_name}.yml"] = yaml.dump(component_playbook, default_flow_style=False)
        
        # Store main playbook
        playbooks["main.yml"] = yaml.dump(main_playbook, default_flow_style=False)
        
        # Generate inventory template
        inventory = {
            "all": {
                "children": {
                    "aws": {
                        "hosts": {},
                        "vars": {
                            "ansible_python_interpreter": "/usr/bin/python3",
                            "ansible_ssh_private_key_file": "~/.ssh/aws_key.pem"
                        }
                    }
                }
            }
        }
        
        # Add component hosts to inventory
        for comp in infra_recommendations.get("infrastructure_recommendations", []):
            component_name = comp["component"].replace(" ", "").lower()
            instance_type = comp.get("aws_ec2_instance_type", "t3.micro")
            inventory["all"]["children"]["aws"]["hosts"][f"{component_name}-{{{{ env }}}}"] = {
                "ansible_host": f"{{{{ lookup('aws_ec2', 'instance_type={instance_type}') }}}}"
            }
        
        playbooks["inventory.yml"] = yaml.dump(inventory, default_flow_style=False)
        
        return playbooks

    def _save_ansible_playbooks(self, repo_path: str, playbooks: Dict[str, str]) -> None:
        """Save Ansible playbooks to the repository"""
        if not repo_path or not os.path.isdir(repo_path):
            logger.warning("No valid repository path provided for saving Ansible playbooks")
            return
            
        # Create ansible directory structure
        ansible_dir = os.path.join(repo_path, "ansible")
        roles_dir = os.path.join(ansible_dir, "roles")
        templates_dir = os.path.join(ansible_dir, "templates")
        
        os.makedirs(ansible_dir, exist_ok=True)
        os.makedirs(roles_dir, exist_ok=True)
        os.makedirs(templates_dir, exist_ok=True)
        
        # Save main playbook and inventory
        for playbook_name, content in playbooks.items():
            if playbook_name in ["main.yml", "inventory.yml"]:
                playbook_path = os.path.join(ansible_dir, playbook_name)
                try:
                    with open(playbook_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info(f"Saved Ansible playbook to {playbook_path}")
                except Exception as e:
                    logger.warning(f"Failed to save Ansible playbook {playbook_name}: {str(e)}")
        
        # Save component playbooks in their respective role directories
        for playbook_name, content in playbooks.items():
            if playbook_name not in ["main.yml", "inventory.yml"]:
                component_name = playbook_name.replace(".yml", "")
                role_dir = os.path.join(roles_dir, component_name)
                tasks_dir = os.path.join(role_dir, "tasks")
                
                os.makedirs(role_dir, exist_ok=True)
                os.makedirs(tasks_dir, exist_ok=True)
                
                playbook_path = os.path.join(tasks_dir, "main.yml")
                try:
                    with open(playbook_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info(f"Saved component playbook to {playbook_path}")
                except Exception as e:
                    logger.warning(f"Failed to save component playbook {playbook_name}: {str(e)}")

    def _deploy_with_ansible(self, repo_path: str, infra_recommendations: Dict[str, Any]) -> str:
        """Deploy infrastructure using Ansible"""
        if not self.aws_credentials:
            return "Error: AWS credentials not available. Please provide credentials first."
        
        try:
            # Generate playbooks if they don't exist
            ansible_dir = os.path.join(repo_path, "ansible")
            if not os.path.exists(os.path.join(ansible_dir, "main.yml")):
                playbooks = self._generate_ansible_playbooks(infra_recommendations)
                self._save_ansible_playbooks(repo_path, playbooks)
            
            # Create ansible.cfg
            ansible_cfg = """[defaults]
inventory = inventory.yml
remote_user = ubuntu
private_key_file = ~/.ssh/aws_key.pem
host_key_checking = False
"""
            
            with open(os.path.join(ansible_dir, "ansible.cfg"), "w") as f:
                f.write(ansible_cfg)
            
            # Run ansible-playbook
            import subprocess
            result = subprocess.run(
                ["ansible-playbook", "main.yml", "-e", f"env=dev aws_region={self.aws_credentials['region_name']}"],
                cwd=ansible_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return f"Deployment completed successfully!\n\nOutput:\n{result.stdout}"
            else:
                return f"Deployment failed!\n\nError:\n{result.stderr}"
                
        except Exception as e:
            logger.error(f"Error deploying with Ansible: {str(e)}", exc_info=True)
            return f"Error deploying with Ansible: {str(e)}"