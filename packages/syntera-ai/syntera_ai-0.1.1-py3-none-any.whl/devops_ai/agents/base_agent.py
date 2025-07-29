import os
from typing import List, Union, Dict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from gitingest import ingest, ingest_from_query, clone_repo, parse_query
import urllib3
import ssl
import httpx  # Change from requests to httpx

# Temporarily disable SSL warnings and certificate verification
# WARNING: This is not recommended for production use
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["SSL_CERT_FILE"] = ""

# Load environment variables
load_dotenv()

class BaseAgent:
    """Base agent class that provides common functionality for all tool agents."""
    
    def __init__(self):
        try:
            # Create httpx client with SSL verification disabled
            http_client = httpx.Client(verify=False)
            
            self.llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-4-turbo-preview",
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                # Use proper httpx client
                http_client=http_client,
            )
            print("ChatOpenAI instance created successfully")
        except Exception as e:
            print(f"Error initializing ChatOpenAI: {str(e)}")
            raise
    
    def analyze_repository(self, repo_path: str, max_file_size: int = 10485760, 
                        include_patterns: Union[List[str], str] = None, 
                        exclude_patterns: Union[List[str], str] = None,
                        output: str = None) -> dict:
        """Analyze GitHub repositories for insights and patterns
        
        Args:
            repo_path: Path to local directory or GitHub repository URL
            max_file_size: Maximum file size in bytes to analyze (default: 10MB)
            include_patterns: List of glob patterns to include (e.g., ['*.py', '*.js'])
            exclude_patterns: List of glob patterns to exclude (e.g., ['**/node_modules/**'])
            output: Optional path to save the analysis results
            
        Returns:
            Dictionary containing repository analysis data
        """
        try:
            # Check if repo_path is a URL or local path
            if repo_path.startswith(('http://', 'https://', 'git@')):
                # Clone the repository if it's a URL
                query = {"url": repo_path}
                print(f"Cloning repository {repo_path} to the active directory...")
                local_path = self.clone_repository(query)
                print(f"Repository cloned successfully to {local_path}")
                repo_path = local_path
            
            # Use gitingest to analyze the repository with advanced parameters
            summary, tree, content = ingest(
                source=repo_path,
                max_file_size=max_file_size,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                output=output
            )
            
            # Return repository information as a dictionary
            return {
                "summary": summary,
                "tree": tree,
                "content": content,
                "repo_info": f"""Repository Summary: {summary}
                
Repository Structure:
{tree}
                
Key Content Insights:
{content}"""
            }
        except Exception as e:
            raise Exception(f"Error analyzing repository: {str(e)}")
    
    def clone_repository(self, query: dict) -> str:
        """Clone a repository from a URL to the current working directory
        
        Args:
            query: Dictionary containing repository URL and optional parameters
                  Example: {"url": "https://github.com/username/repo"}
            
        Returns:
            Path to the cloned repository
        """
        try:
            # Use gitingest to clone the repository
            # Since we want to work with the repository, we'll clone it to the current directory
            import asyncio
            local_path = asyncio.run(clone_repo(query))
            return local_path
        except Exception as e:
            raise Exception(f"Error cloning repository: {str(e)}")
    
    def analyze_from_query(self, query: dict) -> Dict:
        """Analyze a repository based on a query
        
        Args:
            query: Dictionary containing query parameters
                  Example: {
                      "source": "path/to/repo",
                      "max_file_size": 10485760,
                      "from_web": False,
                      "include_patterns": ["*.py", "*.js"],
                      "ignore_patterns": ["**/node_modules/**"]
                  }
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Use gitingest to analyze the repository from query
            result = ingest_from_query(query)
            return result
        except Exception as e:
            raise Exception(f"Error analyzing repository from query: {str(e)}")
    
    def parse_repository_query(self, source: str, max_file_size: int = 10485760, 
                             from_web: bool = False,
                             include_patterns: Union[List[str], str] = None, 
                             ignore_patterns: Union[List[str], str] = None) -> dict:
        """Parse a repository query
        
        Args:
            source: Path to local directory or GitHub repository URL
            max_file_size: Maximum file size in bytes to analyze
            from_web: Whether the source is from the web
            include_patterns: List of glob patterns to include
            ignore_patterns: List of glob patterns to ignore
            
        Returns:
            Dictionary containing parsed query
        """
        try:
            # Use gitingest to parse the query
            query = parse_query(
                source=source,
                max_file_size=max_file_size,
                from_web=from_web,
                include_patterns=include_patterns,
                ignore_patterns=ignore_patterns
            )
            return query
        except Exception as e:
            raise Exception(f"Error parsing repository query: {str(e)}")