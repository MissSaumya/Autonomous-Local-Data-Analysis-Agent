# Autonomous Local Data Analysis Agent

An end-to-end agentic workflow built with **Qwen3 4B** and **LangChain** to perform private, offline data analysis.

## Features
- **Semantic Dataset Recognition**: Automatically identifies famous datasets like Titanic or Iris.
- **Agentic Cleaning**: Uses ReAct logic to handle missing values and duplicates.
- **Automated Visualization**: Generates statistical plots and correlation maps.
- **Privacy-First**: Runs 100% locally via Ollama; no data leaves the machine.

## Tech Stack
- **AI**: LangChain, Ollama (Qwen3 4B)
- **Backend**: Flask, Pandas
- **Frontend**: JavaScript (ES6+), CSS3, HTML5

## Getting Started
1. Install [Ollama](https://ollama.com/) and run `ollama pull qwen3:4b`.
2. Clone this repo.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run: `python app.py`.
