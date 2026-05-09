# Project Title
MCP and Groq Tool Integration
## Project Description
This project provides two independent scripts: one for MCP and Groq tool integration with web search functionality, and another for MCP filesystem reading and README generation using Groq.

## Project Overview
This project contains two main files: `main.py` and `client.py`. 
- `main.py` is responsible for MCP integration, Groq tool calling, and web search agent functionality.
- `client.py` handles MCP filesystem reading and generates README files using Groq.

These files work independently of each other.

## Execution Flow
1. When `main.py` is run, it executes MCP integration, calls the Groq tool, and performs web search operations.
2. When `client.py` is run, it reads the MCP filesystem and generates README files using Groq.

## File-by-File Breakdown
### main.py
- Purpose: Integrate MCP, call Groq tool, and perform web search.
- Main functions: MCP integration, Groq tool calling, web search.
- Behavior: Runs independently to execute MCP, Groq, and web search operations.

### client.py
- Purpose: Read MCP filesystem and generate README using Groq.
- Main functions: MCP filesystem reading, README generation using Groq.
- Behavior: Runs independently to read MCP filesystem and generate README files.

## Features
* MCP filesystem usage
* Groq LLM usage
* Web search tool
* README generation

## Technologies Used
* Python
* Groq API
* MCP
* asyncio

## Installation
1. Install Python and required dependencies.
2. Set up Groq API and MCP.

## Usage
1. Run `main.py` to execute MCP integration, Groq tool calling, and web search.
2. Run `client.py` to read MCP filesystem and generate README files using Groq.

## Project Structure
```markdown
project/
├── main.py
├── client.py
├── README.md
├── .env
```