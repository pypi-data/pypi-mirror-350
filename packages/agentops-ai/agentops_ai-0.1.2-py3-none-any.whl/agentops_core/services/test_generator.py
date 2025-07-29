import ast
import os
from typing import List, Dict, Any, Optional
import openai

class TestGenerator:
    """Service for generating tests using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize the test generator.
        
        Args:
            api_key: OpenAI API key (defaults to env var)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        openai.api_key = self.api_key
    
    def parse_code(self, code: str) -> Dict[str, Any]:
        """Parse Python code to extract structure.
        
        Args:
            code: Python code as string
            
        Returns:
            Dict containing code structure
        """
        try:
            tree = ast.parse(code)
            # Extract classes, functions, etc.
            # Implementation here
            return {"success": True, "structure": {}}
        except SyntaxError as e:
            return {"success": False, "error": str(e)}
    
    def generate_tests(self, code: str, framework: str = "pytest") -> Dict[str, Any]:
        """Generate tests for the given code.
        
        Args:
            code: Python code to generate tests for
            framework: Testing framework to use
            
        Returns:
            Dict containing generated tests and metadata
        """
        # Parse the code
        parsed = self.parse_code(code)
        if not parsed["success"]:
            return {"success": False, "error": parsed["error"]}
        
        # Generate prompt for OpenAI
        prompt = self._create_prompt(code, parsed["structure"], framework)
        
        # Call OpenAI API
        response = self._call_openai(prompt)
        
        # Process and return the generated tests
        return self._process_response(response, framework)
    
    def _create_prompt(self, code: str, structure: Dict[str, Any], framework: str) -> str:
        """Create a prompt for the OpenAI API."""
        summary = []
        if structure:
            # Summarize functions
            functions = structure.get('functions', [])
            if functions:
                summary.append("Functions:")
                for f in functions:
                    summary.append(f"- {getattr(f, 'name', str(f))}({', '.join(p['name'] for p in getattr(f, 'parameters', []))})")
            # Summarize classes
            classes = structure.get('classes', [])
            if classes:
                summary.append("Classes:")
                for c in classes:
                    summary.append(f"- {getattr(c, 'name', str(c))}")
        summary_text = '\n'.join(summary)
        prompt = f"""
Given the following Python code, generate comprehensive {framework} tests. 
- Cover all functions and methods, including edge cases.
- Use clear, idiomatic {framework} style.
- Include docstrings and comments for clarity.
- Output only the test code, no explanations.

Code summary:
{summary_text}

Full code:
"""
        prompt += code
        return prompt
    
    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Call the OpenAI API with the given prompt."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert test engineer. Your task is to generate comprehensive tests for the provided code."},
                    {"role": "user", "content": prompt}
                ]
            )
            return {"success": True, "data": response}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _process_response(self, response: Dict[str, Any], framework: str) -> Dict[str, Any]:
        """Process the OpenAI API response."""
        if not response["success"]:
            return {"success": False, "error": response["error"]}
        data = response["data"]
        # Extract the test code from the OpenAI response
        try:
            test_code = data["choices"][0]["message"]["content"]
            confidence = 1.0 if test_code else 0.0
            return {"success": True, "tests": test_code, "confidence": confidence}
        except Exception as e:
            return {"success": False, "error": f"Failed to parse OpenAI response: {e}"}
    
    def write_tests_to_file(self, test_code: str, output_dir: str = "tests", base_name: str = "test_generated.py") -> str:
        """Write the generated test code to a file and return the file path."""
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, base_name)
        with open(file_path, "w") as f:
            f.write(test_code)
        return file_path 