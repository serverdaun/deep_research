# Deep Research

**Deep Research** is an AI-powered research assistant that helps users investigate complex topics by generating clarifying questions, planning web searches, and synthesizing detailed markdown reports.

## Features

- **Clarification**: Asks targeted questions to refine the research query.
- **Planning**: Suggests up to five web searches to address the query.
- **Web Search**: Summarizes web results for each planned search.
- **Report Generation**: Produces a comprehensive markdown report with a summary and follow-up questions.
- **Interactive UI**: Simple Gradio interface for end-to-end research.

## Usage

1. **Input your research topic** in the UI.
2. **Answer clarifying questions** (if any).
3. **Run the research** to receive a detailed report.

## Tech Stack

- Python, Gradio
- [openai-agents](https://pypi.org/project/openai-agents/) (for agent orchestration)
- Async/await for non-blocking operations

## File Overview

- `main.py` — Gradio UI and app entry point
- `research_manager.py` — Orchestrates the research workflow
- `research_agent.py` — Core agent logic and tool coordination
- `clarifier.py` — Generates clarifying questions
- `planner.py` — Plans web search queries
- `web_search.py` — Summarizes web search results
- `report_generator.py` — Creates the final markdown report

## Setup (with [uv](https://github.com/astral-sh/uv))

1. **Install Python 3.12** (if not already installed).
2. **Install [uv](https://github.com/astral-sh/uv):**
   ```sh
   pip install uv
   ```
3. **Install dependencies:**
   ```sh
   uv pip install -r pyproject.toml
   ```
4. **Run the app:**
   ```sh
   uv pip run python src/main.py
   ```

The app will launch a Gradio interface in your browser.
