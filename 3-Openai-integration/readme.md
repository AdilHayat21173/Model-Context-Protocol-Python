## Groq MCP Server: 

This project demonstrates how to build and utilize an MCP (Model Context Protocol) server integrated with the Groq LLM. The Model Context Protocol acts as a standardized interface, allowing LLMs to securely interact with local tools and data sources.

---

## 🎯 Objectives
* **Create** an MCP server (`server.py`).
* **Test** it using the **MCP Inspector**.
* **Connect** a client (`client.py`).
* **Call tools** like `ask_groq` and `summarize_text`.

---

## 📁 Project Structure
```text
.
├── server.py      # MCP Server with Groq tools
├── client.py      # MCP Client
└── .env           # API key file
```

---

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install mcp groq python-dotenv
```

### 2. Add API Key
Create a `.env` file in your root directory:
```text
GROQ_API_KEY=your_api_key_here
```

---

## 🧠 Step 1: Build & Test Server (IMPORTANT)
Before running the client, verify your server logic using the **MCP Inspector**.

**Run this command:**
```bash
mcp dev server.py
```

> [!IMPORTANT]
> **What this does:**
> * Starts your MCP server in **dev mode**.
> * Opens the **MCP Inspector UI**.
> * Shows available tools for debugging.

**✅ You should see:**
* `ask_groq`
* `summarize_text`

*Test both tools from the UI to ensure they return valid responses from Groq.*

---

## 🚀 Step 2: Run MCP Server
After testing, start the live server:
```bash
python server.py
```

**Expected output:**
`🚀 MCP Server running at http://localhost:8000/mcp`

---

## 🔌 Step 3: Run Client
Open a new terminal and run the client script:
```bash
python client.py
```

### ✅ Expected Output
```text
🔌 Connecting to MCP Server...
✅ Connected!

🛠️  Available Tools:
   - ask_groq: Send a question to Groq LLM and get a response
   - summarize_text: Summarize any given text using Groq

📨 Asking Groq a question...
🤖 Groq says: Python is a high-level, interpreted programming language...
```

---

## 🛠️ Available Tools

| Tool Name | Input | Description |
| :--- | :--- | :--- |
| `ask_groq` | `question` | Returns a direct response from the LLM. |
| `summarize_text` | `text` | Returns a short summary of the provided text. |

---

## 💡 How It Works
* **`server.py`**: Creates the MCP tools and handles the logic for interacting with Groq.
* **`client.py`**: Acts as the interface that connects to the server and calls those tools.
* **MCP**: Functions as a standard bridge between the client and the tools.

---

## ⚠️ Important Notes
* **Always run `mcp dev server.py` first** to ensure your tool definitions are correct.
* **Execution Order:** You must start the **Server** before running the **Client**.
* **API Key:** Ensure your Groq API key is valid and correctly placed in the `.env` file.

---

## 🎯 Quick Summary
1. **Test:** `mcp dev server.py`
2. **Run Server:** `python server.py`
3. **Run Client:** `python client.py`