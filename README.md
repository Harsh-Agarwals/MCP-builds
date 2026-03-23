# Model Context Protocol (MCP) — End-to-End Guide

We are building, using, testing, and implementing MCP servers to fully understand how they work in real-world AI systems.

## Why MCP?

Whenever you build an application on top of LLMs, you need to connect it to data sources. These can be:

* Static data
* Live APIs
* Continuously updating systems

MCP simplifies this by providing a standardized interface (via tools, resources, and prompts) that allows LLMs to securely and efficiently access data.

---

# MCP Ecosystem Overview

There are three core components:

## 1. Host

The environment where everything runs:

* AI tools (e.g., Cursor, GPT-based apps)
* Custom AI software

## 2. MCP Client

* Lives inside the host
* Knows available MCP servers and their capabilities
* Routes requests to the appropriate MCP server

Example:
If a Slack message contains `project-x`, the client decides:

* Which MCP server to call
* What parameters to send

## 3. MCP Server

* Provides access to data
* Exposes tools and resources
* Returns structured outputs

---

# What We Will Learn

We will go beyond simple usage and build MCP systems end-to-end:

1. MCP Protocol
2. Tool Schemas
3. Tool Discovery
4. AI Tool Calling
5. Multi-server Architecture

---

# What We Will Build

## 1. Simple MCP

* Mathematical tools
* Basic resources

## 2. Filesystem MCP

Capabilities:

* Search files
* Read files
* List files
* Summarize files

Architecture:

```
AI Assistant
     |
MCP Client
     |
Filesystem MCP Server
     |
Local Files
```

---

## 3. Database MCP

Capabilities:

* Query data
* Generate reports

Architecture:

```
AI Assistant
     |
MCP Client
     |
Database MCP Server
     |
Postgres / SQLite
```

---

## 4. AI Assistant (Multi-MCP Integration)

Example use case:

> "Compare sales numbers with the forecast document."

Architecture:

```
AI Assistant
     |
MCP Client
     |
----------------------
| Filesystem MCP     |
| Database MCP       |
----------------------
```

---

# Building an MCP Server

## Core Components

### 1. Tools

* Schema-defined functions
* Invoked by LLMs
* Perform a single operation
* Have clear input/output definitions

---

### 2. Resources

* Provide data from:

  * Files
  * APIs
  * Databases
* Help LLM understand context

---

### 3. Prompts

* Predefined instructions injected into LLM
* Used for consistent behavior

---

# Testing MCP Servers

Launch MCP Inspector (GUI):

```bash
mcp dev path_to_mcp_server_file
```

OR

```bash
npx @modelcontextprotocol/inspector path_to_mcp_server_file
```

---

# Connecting MCP to Claude Desktop

Install MCP:

```bash
mcp install path_to_mcp_server_file --name "mcp_name"
```

---

## Claude Config Example

```json
{
  "mcpServers": {
    "finance mcp": {
      "command": "path_to_uv",
      "args": [
        "run",
        "--frozen",
        "--with",
        "mcp[cli]",
        "--with",
        "yfinance",
        "mcp",
        "run",
        "path_to_mcp_server_file"
      ]
    }
  }
}
```

---

## Alternative: Docker-Based MCP

You can also run MCP servers using Docker for better isolation and portability.

---

# Best Practices for MCP Development

## 1. Logging

* Use logging libraries instead of `print`
* Avoid interfering with JSON-RPC outputs

```python
import logging
logger = logging.getLogger(__name__)
```

---

## 2. Timeout Handling

* Prevent long-running or stuck processes

---

## 3. Structured Outputs

* Always return consistent JSON responses

---

## 4. Output Size Control

* Limit rows in large outputs (e.g., CSVs)

---

## 5. Prompt Injection Safety

* Validate inputs carefully
* Avoid blindly trusting user-provided data

---

# Filesystem Safety

Prevent path traversal attacks:

```python
if ".." in name or "/" in name or "\\" in name:
    return json.dumps({"error": "Invalid project name"})
```

---

# Building MCP Client

The MCP client:

* Connects to multiple MCP servers
* Exposes tools to the LLM
* Handles routing and orchestration

---

## Implementations

### 1. `mcp-client/mcp-client.py`

* Uses Weather MCP server
* Returns answers based on user queries

---

### 2. `assistant.py`

* AI assistant for business insights
* Example:

  * Compare sales vs forecast
* Uses:

  * Filesystem MCP
  * Database MCP

---

## Supporting Concepts

A separate Python file is included to understand:

* Context Managers
* `ExitStack`
* `AsyncExitStack`

These are important for:

* Managing multiple MCP connections
* Handling resource cleanup properly

---

# Summary

MCP enables:

* Modular AI systems
* Clean separation of concerns
* Scalable multi-data-source architectures

By building:

* MCP servers
* MCP clients
* Integrated assistants

You gain full control over how AI interacts with data in production systems.
