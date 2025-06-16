---
title: Deep Research
emoji: 🏆
colorFrom: red
colorTo: green
sdk: gradio
sdk_version: 5.34.0
app_file: src/main.py
pinned: false
license: apache-2.0
---

![CD to HF Space](https://github.com/serverdaun/deep_research/actions/workflows/sync-to-hf.yml/badge.svg)

[![View on Hugging Face Spaces](https://img.shields.io/badge/Hugging%20Face-Spaces-blue?logo=huggingface)](https://huggingface.co/spaces/serverdaun/deep-research)

# Deep Research

**Deep Research** is an AI-powered research assistant that helps users investigate complex topics by generating clarifying questions, planning web searches, and synthesizing detailed markdown reports.

## Features

- **Clarification**: Asks targeted questions to refine the research query.
- **Planning**: Suggests up to five web searches to address the query.
- **Web Search**: Summarizes web results for each planned search.
- **Report Generation**: Produces a comprehensive markdown report with a summary and follow-up questions.
- **Interactive UI**: Chat-based Gradio interface for end-to-end research.

## Usage

1. **Send your research topic** in the chat box.
2. **Answer the clarifying questions**.
3. **Receive the detailed report** back in the same conversation.

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
3. **Create enviroment and install dependencies:**
   ```sh
   uv sync
   ```
4. **Activate the enviroment**
   ```sh
   source .venv/bin/activate #.venv/Scripts/activate on Win
   ```
4. **Run the app:**
   ```sh
   uv run src/main.py
   ```

The app will launch a Gradio interface that you can access in your browser.
