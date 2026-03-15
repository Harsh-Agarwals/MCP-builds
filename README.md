# Model Context Protocol

We're building, using, testing and implementing MCP servers here.

Why MCP? Everytime you build an app on the top of LLMs, you need to provide a data source (maybe static or maybe live data source or maybe constantly updating data source) for the app. MCP simplifies this by providing a block of code (with filters) to access specific data from the data source. 

There are three things in MCP ecosystem:
- **Host**: The software/AI stack where everything will be implemented (e.g. Cursor, GPT, AI software, etc)
- **MCP Client**: Rests inside host system and is given access to MCPs available along with their features, functions, etc. When client gets request for any access (like message from slack channel having keyword `project-x`), MCP client decide what server to send request to along with the parameters required.
- **MCP Server**: Provides access to data asked by MCP client to the host. It can return data, exposes tools and resources, etc.

Here, we will not just integrate MCPs into our workflow to build simple applications, but also build MCP clients and servers from scratch for end-to-end ecosystem understanding and understanding nuances of MCPs. We'll understand:

1️⃣ *MCP protocol*
2️⃣ *tool schemas*
3️⃣ *tool discovery*
4️⃣ *AI tool calling*
5️⃣ *multi-server architecture*

We'll build:
|- **Simple MCP** for simple mathematical functions as tools and resources
|- **filesystem MCP** [search files, read files, list files, summarize files]
|- **database MCP** [query data, generate report]
|- **AI assistants** utilizing some built-in and external MCP servers (eg. using filesystem and database MCPs like *"Compare sales numbers with the forecast document."*)

## Filesystem MCP
AI assistant
     |
MCP client
     |
filesystem MCP server
     |
local files

## Database MCP
AI assistant
     |
MCP client
     |
database MCP server
     |
Postgres / SQLite

## AI Assistant
AI assistant
     |
MCP client
     |
----------------------
| filesystem MCP     |
| database MCP       |
----------------------

### Building MCP server:

#### Components:
- **Tools**: Tools are schema-defined interfaces that LLMs can invoke. Each tool performs a single operation with clearly defined inputs and outputs.
- **Resources**: Resources expose data from files, APIs, databases, or any other source that an AI needs to understand context. Applications can access this information directly and decide how to use it. 
- **Tools**: