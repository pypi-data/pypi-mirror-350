API Reference
=============

This section provides detailed API reference documentation for Python A2A.

Core Components
--------------

Python A2A is organized into several core components:

1. **Models**: Data structures for messages, tasks, and agent cards
2. **Client**: Components for connecting to A2A agents
3. **Server**: Components for building A2A-compatible agents
4. **Discovery**: Registry and discovery for finding A2A agents
5. **MCP**: Tools for implementing Model Context Protocol
6. **Utils**: Helper functions for common tasks

Models
------

.. toctree::
   :maxdepth: 2
   
   models

Models include:

- ``Message`` - Represents an A2A message
- ``Conversation`` - Represents a conversation of messages
- ``AgentCard`` - Describes an agent and its capabilities
- ``AgentSkill`` - Describes a skill that an agent provides
- ``Task`` - Represents a unit of work in the A2A protocol

Client
------

.. toctree::
   :maxdepth: 2
   
   client

Client components include:

- ``A2AClient`` - HTTP client for connecting to A2A agents
- ``OpenAIA2AClient`` - Client for OpenAI-based A2A agents
- ``AnthropicA2AClient`` - Client for Anthropic-based A2A agents

Server
------

.. toctree::
   :maxdepth: 2
   
   server

Server components include:

- ``A2AServer`` - Base server for A2A agents
- ``OpenAIA2AServer`` - Server that uses OpenAI's API
- ``AnthropicA2AServer`` - Server that uses Anthropic's API
- ``BedrockA2AServer`` - Server that uses AWS Bedrock

Discovery
--------

.. toctree::
   :maxdepth: 2
   
   discovery

Discovery components include:

- ``AgentRegistry`` - Server for agent discovery
- ``DiscoveryClient`` - Client for interacting with registry servers
- ``enable_discovery`` - Function to add discovery to existing servers
- ``RegistryAgent`` - Combined agent and registry server

MCP Integration
--------------

.. toctree::
   :maxdepth: 2
   
   mcp

MCP components include:

- ``FastMCP`` - Implementation of MCP server
- ``MCPClient`` - Client for connecting to MCP servers
- ``A2AMCPAgent`` - A2A agent with MCP capabilities

Utilities
---------

.. toctree::
   :maxdepth: 2
   
   utils

Utility functions include:

- Formatting utilities
- Validation utilities
- Conversion utilities
- Decorator functions