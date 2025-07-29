from typing import List, Union, Dict, Any
from .base_agent import BaseAgent
import os
import json
import logging
import datetime
from pathlib import Path
from git import Repo
from github import Github
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DockerGenerationAgent(BaseAgent):
    """Agent for generating Docker and docker-compose files based on repository analysis"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    def analyze(self, repo_path: str, max_file_size: int = 10485760,
                include_patterns: Union[List[str], str] = None,
                exclude_patterns: Union[List[str], str] = None,
                output: str = None) -> str:
        """Analyze repository structure and generate Docker files"""
        try:
            abs_repo_path = os.path.abspath(repo_path)
            logger.info(f"Starting analysis for repo: {repo_path}")
            logger.info(f"Absolute path: {abs_repo_path}")
            logger.info(f"Directory exists: {os.path.isdir(abs_repo_path)}")

            repo_data = self.analyze_repository(
                repo_path=repo_path,
                max_file_size=max_file_size,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                output=output
            )

            if 'repo_path' not in repo_data:
                repo_data['repo_path'] = abs_repo_path

            dockerfile_content, compose_content = self._generate_docker_files(repo_data)

            logger.info(f"Docker files generated. Services: {list(dockerfile_content.keys())}")
            logger.info(f"Compose content length: {len(compose_content) if compose_content else 0}")

            self._write_docker_files(abs_repo_path, dockerfile_content, compose_content)

            return f"Successfully generated Docker files for {repo_path}:\n" + \
                   f"Dockerfile(s): {', '.join(list(dockerfile_content.keys()))}\n" + \
                   f"docker-compose.yml: {'Created' if compose_content else 'Not created'}"

        except Exception as e:
            logger.error(f"Error generating Docker files: {str(e)}", exc_info=True)
            return f"Error generating Docker files: {str(e)}"

    def _generate_docker_files(self, repo_data: Dict[str, Any]) -> tuple:
        """Generate Dockerfile(s) and docker-compose.yml content using LangChain + OpenAI"""
        repo_structure = repo_data.get('tree', {})
        repo_path = repo_data.get('repo_path', None)

        logger.debug(f"[DEBUG] Repository structure (tree): {repo_structure}")

        # Extract contents of key files for better LLM context
        key_files = []
        if repo_path:
            for root, _, files in os.walk(repo_path):
                for fname in files:
                    if fname.lower() in {
                        "requirements.txt", "package.json", "pom.xml", "build.gradle",
                        "composer.json", "gemfile", "cargo.toml", "setup.py",
                        "environment.yml", "pipfile", "makefile", "dockerfile"
                    } or fname.endswith((
                        ".py", ".js", ".ts", ".go", ".java", ".cs", ".rb", ".php", ".rs",
                        ".cpp", ".c", ".sh", ".pl", ".scala", ".kt", ".swift", ".dart",
                        ".m", ".r", ".jl", ".ex", ".exs", ".clj", ".cljs", ".groovy",
                        ".lua", ".hs", ".sql", ".json", ".yml", ".yaml"
                    )):
                        key_files.append(os.path.relpath(os.path.join(root, fname), repo_path))

        file_contents = {}
        if repo_path:
            for fname in key_files[:10]:  # Limit to 10 files for prompt size
                fpath = os.path.join(repo_path, fname)
                if os.path.exists(fpath):
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            file_contents[fname] = f.read()[:2000]
                    except Exception as e:
                        file_contents[fname] = f"[Error reading file: {e}]"

        prompt = f"""Analyze the following repository structure and key file contents. Detect the main programming languages, frameworks, and build tools.

Generate appropriate Dockerfile(s) and a docker-compose.yml for the detected services.
Follow these guidelines strictly:
- Prefer multi-stage builds where applicable
- Use non-root users and minimal base images
- Include labels like maintainer, version, and description
- Avoid invalid syntax and assumptions about stack
- If unsure, clearly explain why and do not generate invalid files

Repository Structure:
{repo_structure}
"""

        if file_contents:
            prompt += "\nKey file contents:\n"
            for fname, content in file_contents.items():
                prompt += f"--- {fname} ---\n{content}\n"

        prompt += """
Please provide your response in the following JSON format, wrapped in triple backticks:
```json
{
    "analysis": "Your analysis of technologies used",
    "dockerfiles": {
        "service_name1": "Dockerfile content",
        "service_name2": "Dockerfile content"
    },
    "docker_compose": "Multi-service compose configuration"
}
If you cannot confidently generate valid Docker content, state it clearly in the analysis field.
"""

        logger.debug(f"[DEBUG] LLM prompt: {prompt}")

        # LangChain integration
        response = self.llm.invoke([HumanMessage(content=prompt)])
        response_text = response.content.strip()

        logger.debug(f"[DEBUG] Raw LLM response: {response_text[:200]}...")

        # Extract JSON from possible markdown
        if "```json" in response_text:
            start_idx = response_text.find("```json") + 7
            end_idx = response_text.rfind("```")
            if end_idx > start_idx:
                response_text = response_text[start_idx:end_idx].strip()
                logger.debug(f"[DEBUG] Extracted JSON from backticks: {response_text[:100]}...")
        elif response_text.startswith("```"):
            start_idx = response_text.find("```") + 3
            end_idx = response_text.rfind("```")
            if end_idx > start_idx:
                response_text = response_text[start_idx:end_idx].strip()
                logger.debug(f"[DEBUG] Extracted general backtick content: {response_text[:100]}...")

        try:
            result = json.loads(response_text)
            dockerfiles = result.get("dockerfiles", {})
            docker_compose = result.get("docker_compose", "").strip()

            logger.debug(f"[DEBUG] Successfully parsed JSON. Found {len(dockerfiles)} Dockerfiles.")

            # Validate content
            if not dockerfiles or any('generation failed' in v.lower() or not v.strip() for v in dockerfiles.values()):
                logger.error(f"[ERROR] Invalid Dockerfile content: {dockerfiles}")
                raise ValueError("Invalid Dockerfile content generated.")

            if not docker_compose or 'generation failed' in docker_compose.lower():
                logger.error(f"[ERROR] Invalid docker-compose content: {docker_compose[:100]}")
                raise ValueError("Invalid docker-compose.yml content generated.")

            return dockerfiles, docker_compose

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Problematic JSON: {response_text}")
            return {}, ""

    def _write_docker_files(self, repo_path: str, dockerfiles: dict, compose_content: str) -> None:
        """Write Dockerfile(s), docker-compose.yml, and supporting files to the repository"""
        try:
            if repo_path.startswith(('http://', 'https://', 'git@')):
                raise ValueError("Repository path must be a local directory")

            logger.debug(f"Writing Docker files to {repo_path}")
            logger.debug(f"Dockerfiles to write: {list(dockerfiles.keys()) if dockerfiles else 'None'}")

            if not os.path.isdir(repo_path):
                logger.error(f"Repository path is not a directory: {repo_path}")
                raise ValueError(f"Invalid repository path: {repo_path}")

            if not dockerfiles:
                logger.error("No Dockerfiles generated. Cannot proceed.")
                raise ValueError("No Dockerfiles generated. Cannot proceed.")

            # Write Dockerfiles
            for service, content in dockerfiles.items():
                dockerfile_path = os.path.join(repo_path, f"Dockerfile.{service}")
                logger.info(f"Writing Dockerfile for {service} to {dockerfile_path}")
                with open(dockerfile_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.debug(f"Successfully wrote {dockerfile_path}")

            # Write docker-compose.yml
            if compose_content:
                compose_path = os.path.join(repo_path, "docker-compose.yml")
                logger.info(f"Writing docker-compose.yml to {compose_path}")
                with open(compose_path, "w", encoding="utf-8") as f:
                    f.write(compose_content)
                logger.debug(f"Successfully wrote {compose_path}")

            # Generate .dockerignore
            self._generate_dockerignore(repo_path)

            # Generate README-Docker.md
            self._generate_docker_readme(repo_path, dockerfiles)

            # Generate GitHub Actions CI/CD workflow
            self._generate_github_actions_workflow(repo_path)

            # Save analysis log
            self._save_analysis_log(repo_path, dockerfiles, compose_content)

        except Exception as e:
            logger.error(f"Error in _write_docker_files: {str(e)}", exc_info=True)
            raise

    def _generate_dockerignore(self, repo_path: str):
        default_ignore = """
.git
__pycache__
*.log
*.env
.env
node_modules
*.pyc
*.tmp
*.bak
*.swp
*.swo
*.DS_Store
Thumbs.db
*.md
README.md
"""

        dockerignore_path = os.path.join(repo_path, ".dockerignore")
        if not os.path.exists(dockerignore_path):
            with open(dockerignore_path, "w", encoding="utf-8") as f:
                f.write(default_ignore.strip())
            logger.info(f"Generated .dockerignore at {dockerignore_path}")

    def _generate_docker_readme(self, repo_path: str, dockerfiles: dict):
        services = "\n".join([f"- `{k}`" for k in dockerfiles.keys()])
        content = f"""# Docker Setup Guide

This document was auto-generated by the Docker Generation Agent.

## Available Services
{services}

## How to Use

### Build all services:
```bash
docker-compose build
```

### Run all services:
```bash
docker-compose up -d
```

### Build individual service:
```bash
docker build -t <service-name> -f Dockerfile.<service-name> .
```

### View logs:
```bash
docker-compose logs -f
```

For more info see: https://docs.docker.com/
"""

        readme_path = os.path.join(repo_path, "README-Docker.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Generated README-Docker.md at {readme_path}")

    def _generate_github_actions_workflow(self, repo_path: str):
        workflow_dir = os.path.join(repo_path, ".github", "workflows")
        os.makedirs(workflow_dir, exist_ok=True)

        workflow_content = """name: Docker Build and Push
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_TOKEN }}
      - name: Build and push
        id: docker_build
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: your-dockerhub-username/your-image:latest
"""

        workflow_path = os.path.join(workflow_dir, "docker-build.yml")
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(workflow_content)
        logger.info(f"Generated GitHub Actions workflow at {workflow_path}")

    def _save_analysis_log(self, repo_path: str, dockerfiles: dict, compose_content: str):
        log_content = {
            "timestamp": datetime.datetime.now().isoformat(),
            "dockerfiles": list(dockerfiles.keys()),
            "docker_compose_present": bool(compose_content),
            "llm_model": "gpt-4o-mini"
        }

        log_path = os.path.join(repo_path, ".docker-generation.log.json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_content, f, indent=2)
        logger.info(f"Saved analysis log to {log_path}")

    def push_to_github(self, repo_path: str, token: str, commit_message: str = "Auto-generated Docker files"):
        g = Github(token)
        repo_name = os.path.basename(os.path.abspath(repo_path))
        remote_url = f"https://github.com/<your-org-or-user>/{repo_name}.git"

        repo = Repo.init(repo_path)
        repo.index.add(["Dockerfile.*", "docker-compose.yml", "README-Docker.md", ".dockerignore", ".docker-generation.log.json", ".github/workflows/docker-build.yml"])
        repo.index.commit(commit_message)

        origin = repo.create_remote("origin", remote_url)
        origin.push()
        logger.info(f"Successfully pushed Docker files to GitHub: {remote_url}")

#automtically append secrets key in the docker files