# 🔬 Multi-Agent AI Research System (ResearchMind)

ResearchMind is a fully autonomous, multi-agent AI research pipeline built with [LangChain](https://python.langchain.com/) and powered by **Mistral AI**. It features a sleek, responsive [Streamlit](https://streamlit.io/) interface that visually tracks the progress of specialized AI agents as they gather, process, write, and critique a comprehensive research report on any given topic.

## ✨ Features

- **Multi-Agent Architecture**: Divides the complex task of research into specialized, focused agents.
- **Real-time Web Search**: Uses the **Tavily API** to find the most recent and reliable information online.
- **Deep Web Scraping**: Automatically extracts and cleans text from relevant URLs using **BeautifulSoup**.
- **Automated Critique & Scoring**: A dedicated Critic Agent reviews the generated report to ensure accuracy, highlighting strengths and areas for improvement.
- **Beautiful UI**: A highly polished, custom-styled Streamlit frontend featuring progress tracking, score badges, and downloadable reports.

## 🏗️ Architecture & Agents

The system orchestrates a pipeline (`pipeline.py`) of four distinct steps:

1. **🔍 Search Agent**: Takes the user's topic and queries the web to find relevant, up-to-date sources and snippets (`tools.py` -> `web_search`).
2. **📄 Reader Agent**: Analyzes the search results, identifies the most promising URL, and scrapes its deep content (`tools.py` -> `scrape_url`).
3. **✍️ Writer Chain**: Synthesizes the gathered search snippets and scraped text into a well-structured, professional markdown report (`agents.py`).
4. **🧐 Critic Agent**: Reviews the final report, providing a score out of 10, outlining strengths, areas to improve, and a final verdict (`agents.py`).

## 🚀 Getting Started

### Prerequisites

You will need API keys for the following services:
- **Mistral AI API Key** (for the LLM)
- **Tavily API Key** (for web searching)

### Installation

1. **Clone the repository** (or download the files).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
MISTRAL_API_KEY="your_mistral_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
MISTRAL_MODEL="mistral-small-latest" # Optional: can also be set in the UI
```

## 🎮 Usage

Run the Streamlit application using the following command:

```bash
python -m streamlit run app.py
```

1. Open the provided Local URL in your web browser (usually `http://localhost:8501`).
2. Enter your **Mistral API Key** in the sidebar (if not set in the `.env` file).
3. Type a **Research Topic** (e.g., "Quantum computing breakthroughs in 2025").
4. Click **Run Pipeline** and watch the agents work in sequence.
5. Once finished, view the search results, scraped content, the final report, and the critic's review. You can also **download the report as a `.md` file**.

## 📂 Codebase Overview

- `app.py`: The main Streamlit application, containing the custom UI, state management, and pipeline execution logic.
- `pipeline.py`: The orchestration layer that connects the agents and yields progress back to the UI.
- `agents.py`: The LangChain setup, defining the specific prompts, models, and chains for the search, read, write, and critic agents.
- `tools.py`: Custom LangChain tools (`web_search` and `scrape_url`) used by the agents to interact with the outside world.
- `requirements.txt`: The project dependencies.

## 🛠️ Built With

- **[LangChain](https://www.langchain.com/)** - Framework for developing LLM-powered applications
- **[Mistral AI](https://mistral.ai/)** - Large Language Models
- **[Streamlit](https://streamlit.io/)** - Frontend framework for Python
- **[Tavily](https://tavily.com/)** - Search engine optimized for AI agents
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** - Web scraping library