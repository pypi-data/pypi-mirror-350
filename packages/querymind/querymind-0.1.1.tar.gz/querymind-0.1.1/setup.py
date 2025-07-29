from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="querymind",
    version="0.1.1",
    author="Ra-Is",
    author_email="osumanurais@gmail.com",
    description="Ask natural language questions about your CSV data using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ra-is/querymind",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
    ],
    keywords=[
        "pandas",
        "ai",
        "llm",
        "openai",
        "anthropic",
        "data-analysis",
        "natural-language",
    ],
    project_urls={
        "Bug Reports": "https://github.com/ra-is/querymind/issues",
        "Source": "https://github.com/ra-is/querymind",
    },
) 