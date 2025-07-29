LangChain API Reference
======================

This section provides detailed API documentation for the LangChain integration module.

ToolServer
---------

.. autoclass:: python_a2a.langchain.ToolServer
   :members:
   :inherited-members:
   :special-members: __init__

   .. automethod:: register_tool
   .. automethod:: register_tools
   .. automethod:: from_tools
   .. automethod:: from_toolkit

LangChainBridge
-------------

.. autoclass:: python_a2a.langchain.LangChainBridge
   :members:
   :inherited-members:

   .. automethod:: agent_to_a2a
   .. automethod:: agent_to_tool
   .. automethod:: mcp_to_tools

AgentFlow
--------

.. autoclass:: python_a2a.langchain.AgentFlow
   :members:
   :inherited-members:
   :special-members: __init__

   .. automethod:: add_langchain_step
   .. automethod:: add_tool_step
   .. automethod:: add_a2a_tool_step

Module Functions
--------------

.. automodule:: python_a2a.langchain
   :members:
   :exclude-members: ToolServer, LangChainBridge, AgentFlow