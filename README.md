# 🤖 Jarvis AI Agent

A simple AI agent built from scratch in Python using the Groq API, `openai/gpt-oss-20b`, and Playwright.

The goal of this project is to understand how AI agents actually work by building the core agent loop manually instead of relying on large frameworks.

## 🚀 Current Capabilities

Jarvis can:

* Chat naturally using Groq
* Perform mathematical calculations
* Get the current time for a timezone
* Open URLs in Chrome, Edge, or Brave
* Control a persistent Chrome browser with Playwright
* Search YouTube using browser automation
* Open YouTube videos
* Play YouTube videos
* Perform multi-step tool calling

### Example

```text
User:
Find MrBeast's latest video and play it

Jarvis:
1. Searches YouTube
2. Reads real search results
3. Selects a video
4. Opens the video
5. Clicks the play button
6. Returns the result
```

## 🧠 Agent Architecture

```text
User
  ↓
Groq LLM
  ↓
Decide whether a tool is needed
  ↓
Python tool
  ↓
Tool result
  ↓
Groq LLM
  ↓
Final response
```

For multi-step tasks, the agent continues the loop:

```text
User
  ↓
LLM
  ↓
Tool
  ↓
LLM
  ↓
Tool
  ↓
LLM
  ↓
Final answer
```

## 📁 Project Structure

```text
Jarvis/
│
├── main.py
├── tools.py
├── browser.py
├── browser_test.py
├── README.md
└── .gitignore
```

### `main.py`

Handles:

* Groq API communication
* Conversation history
* Tool definitions
* Tool dispatching
* Agent loop
* Token tracking

### `tools.py`

Contains the Python tools Jarvis can use:

* `open_browser`
* `calculate`
* `get_time`
* `browser_open`
* `browser_search`
* `browser_play`

### `browser.py`

Contains the Playwright browser controller and persistent Chrome session.

## 🛠️ Requirements

* Python 3.10+
* Groq API key
* Google Chrome
* Playwright

Install Playwright:

```bash
pip install playwright
python -m playwright install
```

Install the Groq Python SDK:

```bash
pip install groq
```

## 🔐 API Key Setup

Set your Groq API key as an environment variable.

### Windows CMD

```cmd
set GROQ_API_KEY=your_api_key_here
```

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

Do **not** put your API key directly into the source code.

## ▶️ Run Jarvis

```bash
python main.py
```

Then interact with Jarvis from the terminal.

Example:

```text
You: what is 25 * 16?

Jarvis: The answer is 400.
```

```text
You: search youtube for MrBeast

Jarvis: ...
```

## 🔧 Current Tools

| Tool             | Purpose                                     |
| ---------------- | ------------------------------------------- |
| `open_browser`   | Launch a URL in Chrome, Edge, or Brave      |
| `browser_open`   | Open a URL in the controlled Chrome session |
| `browser_search` | Search YouTube using Playwright             |
| `browser_play`   | Play the currently open YouTube video       |
| `calculate`      | Perform arithmetic                          |
| `get_time`       | Get the current time                        |

## 📊 Learning Goals

This project is being built to understand:

* LLM tool calling
* Agent loops
* Function execution
* Tool schemas
* Conversation state
* Token usage
* Browser automation
* LLM + external tool orchestration

## 🚧 Roadmap

Planned improvements:

* `browser_read()`
* `browser_click()`
* Better page inspection
* More reliable video selection
* General web navigation
* More browser actions
* Better error recovery
* Improved memory/state handling
* More useful desktop automation

## ⚠️ Notes

This is a learning project and is actively being developed.

The browser automation currently focuses mainly on YouTube and Chrome.

## 📜 License

This project is currently intended for personal learning and experimentation.
