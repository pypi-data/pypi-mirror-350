# QueryMind

Ask natural language questions about your CSV data using AI. This package intelligently translates your questions into pandas code using Large Language Models (LLMs) and provides clear, concise answers.

## Features

- 🤖 Natural language to pandas code translation
- 🔒 Safe code execution in a controlled environment
- 📊 Optional result summarization in natural language
- 🔌 Support for multiple LLM providers (OpenAI and Anthropic)
- 🛠️ Clean, maintainable, and extensible design

## Installation

```bash
pip install querymind
```

## Quick Start

```python
from querymind import AIQuery

# Initialize with your CSV file and preferred LLM provider
ai = AIQuery(
    csv_path="your_data.csv",
    llm_provider="openai",  # or "anthropic"
    api_key="your-api-key"
)

# Ask questions in natural language
result = ai.ask("What is the average age of customers who made purchases over $100?")
print(result)

# Get raw results without summarization
raw_result = ai.ask("Show me the top 5 products by sales", summarize=False)
print(raw_result)
```

## Supported LLM Providers

### OpenAI

- Uses GPT-4 for code generation and summarization
- Requires an OpenAI API key

### Anthropic

- Uses Claude 3 Opus for code generation and summarization
- Requires an Anthropic API key

## Example Questions

Here are some example questions you can ask:

- "What is the average salary by department?"
- "Show me the top 10 customers by total purchase amount"
- "How many products are out of stock?"
- "What is the correlation between age and purchase amount?"
- "List all transactions from last month"

## Security

The package executes generated code in a controlled environment with limited access to:

- The pandas DataFrame (`df`)
- The pandas library (`pd`)
- No access to other Python built-ins or system resources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
