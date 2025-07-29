MCP API
=======

This page documents the Model Context Protocol (MCP) API of Python A2A.

MCP Client
---------

.. autoclass:: python_a2a.mcp.MCPClient
   :members:
   :undoc-members:
   :show-inheritance:

FastMCP
------

.. autoclass:: python_a2a.mcp.FastMCP
   :members:
   :undoc-members:
   :show-inheritance:

MCPResponse
----------

.. autoclass:: python_a2a.mcp.MCPResponse
   :members:
   :undoc-members:
   :show-inheritance:

Response Helpers
--------------

.. autofunction:: python_a2a.mcp.text_response

.. autofunction:: python_a2a.mcp.error_response

.. autofunction:: python_a2a.mcp.image_response

.. autofunction:: python_a2a.mcp.multi_content_response

MCP Agent Integration
-------------------

Original MCP Agent
~~~~~~~~~~~~~~~~

.. autoclass:: python_a2a.mcp.MCPEnabledAgent
   :members:
   :undoc-members:
   :show-inheritance:

Fast MCP Agent
~~~~~~~~~~~~

.. autoclass:: python_a2a.mcp.FastMCPAgent
   :members:
   :undoc-members:
   :show-inheritance:

A2A MCP Agent
~~~~~~~~~~~

.. autoclass:: python_a2a.mcp.A2AMCPAgent
   :members:
   :undoc-members:
   :show-inheritance:

MCP Errors
---------

.. autoclass:: python_a2a.mcp.MCPError
   :members:
   :show-inheritance:

.. autoclass:: python_a2a.mcp.MCPConnectionError
   :members:
   :show-inheritance:

.. autoclass:: python_a2a.mcp.MCPTimeoutError
   :members:
   :show-inheritance:

.. autoclass:: python_a2a.mcp.MCPToolError
   :members:
   :show-inheritance:

Proxy Functionality
-----------------

.. autofunction:: python_a2a.mcp.create_proxy_server

Transport
--------

.. autofunction:: python_a2a.mcp.create_fastapi_app