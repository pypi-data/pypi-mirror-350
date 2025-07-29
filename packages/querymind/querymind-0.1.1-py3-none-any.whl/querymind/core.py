"""
Core functionality for AI-Pandas-Query.
"""

import pandas as pd
import json
from typing import Any, Optional, Dict, List
from .llms import get_llm

class AIQueryError(Exception):
    """Base exception for AIQuery errors."""
    pass

class DataFrameError(AIQueryError):
    """Exception for DataFrame-related errors."""
    pass

class CodeExecutionError(AIQueryError):
    """Exception for code execution errors."""
    pass

class AIQuery:
    """
    Main class for querying pandas DataFrames using natural language.
    """
    
    SUPPORTED_PROVIDERS = ["openai", "anthropic"]
    
    def __init__(self, csv_path: str, llm_provider: str, api_key: str):
        """
        Initialize AIQuery with a CSV file and LLM provider.
        
        Args:
            csv_path: Path to the CSV file
            llm_provider: Name of the LLM provider ("openai" or "anthropic")
            api_key: API key for the LLM provider
            
        Raises:
            ValueError: If the provider is not supported
            DataFrameError: If there are issues with the CSV file
        """
        if llm_provider.lower() not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported LLM provider: {llm_provider}. "
                f"Supported providers are: {', '.join(self.SUPPORTED_PROVIDERS)}"
            )
        
        try:
            self.df = pd.read_csv(csv_path)
            self._validate_dataframe()
        except Exception as e:
            raise DataFrameError(f"Error loading CSV file: {str(e)}")
            
        self.llm = get_llm(llm_provider, api_key)
    
    def _validate_dataframe(self) -> None:
        """
        Validate the DataFrame structure and content.
        
        Raises:
            DataFrameError: If the DataFrame is invalid
        """
        if self.df.empty:
            raise DataFrameError("The CSV file is empty")
            
        if len(self.df.columns) == 0:
            raise DataFrameError("The CSV file has no columns")
            
        # Check for missing values
        missing_values = self.df.isnull().sum()
        if missing_values.any():
            print(f"Warning: Found missing values in columns: {missing_values[missing_values > 0].to_dict()}")
    
    def _safe_execute_code(self, code: str) -> Any:
        """
        Safely execute the generated pandas code.
        
        Args:
            code: The pandas code to execute
            
        Returns:
            The result of the code execution
            
        Raises:
            CodeExecutionError: If there are issues executing the code
        """
        try:
            # Create a safe environment for code execution
            safe_dict = {"df": self.df, "pd": pd}
            result = eval(code, {"__builtins__": {}}, safe_dict)
            return result
        except Exception as e:
            raise CodeExecutionError(f"Error executing pandas code: {str(e)}\nGenerated code: {code}")
    
    def ask(self, question: str, summarize: bool = True) -> Any:
        """
        Ask a natural language question about the data.
        
        Args:
            question: Natural language question about the data
            summarize: Whether to summarize the result in natural language
            
        Returns:
            The result of the query, optionally summarized
            
        Raises:
            AIQueryError: If there are any issues during the query process
        """
        try:
            # Validate input
            if not question or not isinstance(question, str):
                raise ValueError("Question must be a non-empty string")
            
            # Generate and execute code
            prompt = self._construct_prompt(question)
            code = self.llm.generate_code(prompt)
            result = self._safe_execute_code(code)
            
            # Handle empty results
            if result is None:
                return "No results found for your query."
            
            # Handle empty DataFrame results
            if isinstance(result, pd.DataFrame) and result.empty:
                return "The query returned no data."
            
            # Summarize if requested
            if summarize:
                try:
                    return self.llm.summarize(result)
                except Exception as e:
                    print(f"Warning: Could not summarize result: {str(e)}")
                    return result
            
            return result
            
        except AIQueryError as e:
            raise
        except Exception as e:
            raise AIQueryError(f"Unexpected error: {str(e)}")
    
    def _construct_prompt(self, question: str) -> str:
        """
        Construct a prompt for the LLM.
        
        Args:
            question: Natural language question
            
        Returns:
            Formatted prompt for the LLM
        """
        try:
            # Get DataFrame information
            columns = self.df.columns.tolist()
            dtypes = {col: str(dtype) for col, dtype in self.df.dtypes.items()}
            sample_data = self.df.head(3).to_dict('records')
            
            # Format the data for better readability
            sample_data_str = json.dumps(sample_data, indent=2)
            
            # Construct the prompt with DataFrame information
            return f"""You are a pandas expert. Given this question about a DataFrame called 'df':

"{question}"

Here is the structure of the DataFrame:
- Columns: {columns}
- Data types: {dtypes}
- Sample data (first 3 rows): 
{sample_data_str}

Write pandas code to answer this question. The code should:
1. Use only the DataFrame 'df' and pandas (pd)
2. Be a single expression or statement
3. Return the exact answer to the question
4. Use the correct column names as shown above
5. Handle potential missing values appropriately

Code:"""
        except Exception as e:
            raise AIQueryError(f"Error constructing prompt: {str(e)}") 