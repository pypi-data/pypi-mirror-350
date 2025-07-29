from .base_agent import BaseAgent

class LogAnalysisAgent(BaseAgent):
    """Agent for analyzing log files for errors and patterns"""
    
    def analyze(self, log_file: str, repo_path: str = None) -> str:
        """Analyze log files for errors and patterns
        
        Args:
            log_file: Path to the log file to analyze
            repo_path: Optional path to repository for context
            
        Returns:
            Analysis of log file
        """
        try:
            # Read log file content
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            # Get repository context if provided
            repo_context = ""
            if repo_path:
                try:
                    repo_data = self.analyze_repository(repo_path)
                    repo_context = f"\n\nRepository Context:\n{repo_data['summary']}"
                except:
                    pass
            
            # Generate analysis using LLM
            prompt = f"""Analyze the following log file and provide insights:{repo_context}
            {log_content}
            
            Please provide:
            1. Error patterns
            2. Critical issues
            3. Performance bottlenecks
            4. Recommendations
            """
            
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error analyzing logs: {str(e)}"