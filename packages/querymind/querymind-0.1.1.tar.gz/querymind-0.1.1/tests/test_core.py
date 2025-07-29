"""
Tests for the core AIQuery functionality.
"""

import unittest
import pandas as pd
import os
from aipandasquery import AIQuery

class TestAIQuery(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 70000]
        })
        
        # Save to a temporary CSV file
        self.csv_path = 'test_data.csv'
        self.df.to_csv(self.csv_path, index=False)
        
        # Mock API key
        self.api_key = "test-api-key"
    
    def tearDown(self):
        # Clean up the temporary CSV file
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
    
    def test_initialization(self):
        """Test that AIQuery initializes correctly."""
        ai = AIQuery(self.csv_path, "openai", self.api_key)
        self.assertIsNotNone(ai)
        self.assertTrue(isinstance(ai.df, pd.DataFrame))
    
    def test_invalid_provider(self):
        """Test that an invalid provider raises an error."""
        with self.assertRaises(ValueError):
            AIQuery(self.csv_path, "invalid_provider", self.api_key)
    
    def test_invalid_csv_path(self):
        """Test that an invalid CSV path raises an error."""
        with self.assertRaises(FileNotFoundError):
            AIQuery("nonexistent.csv", "openai", self.api_key)

if __name__ == '__main__':
    unittest.main() 