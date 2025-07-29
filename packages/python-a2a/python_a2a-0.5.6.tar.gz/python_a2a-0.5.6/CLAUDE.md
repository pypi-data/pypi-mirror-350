# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Design Philosophy
- Avoid monkey patching - implement proper solutions following standards
- MCP (Model Context Protocol) uses JSON-RPC 2.0 as its wire protocol, not REST
- Support multiple transports (stdio, SSE) through clean abstractions, not separate client classes
- Maintain backward compatibility where possible but prioritize correctness

## Build Commands
- Build project: `make build`
- Lint code: `make lint`
- Run all tests: `make test`
- Run single test: `pytest tests/test_file.py::TestClass::test_function -v`
- Format code: `make format`
- Setup dev environment: `uv venv && uv install -e ".[dev]"`
- Validate examples: `python examples/validate_all_examples.py`

## Code Style
- Python >=3.9 compatibility
- Black formatting with 88 character line limit
- isort with Black profile for import ordering
- Strict type annotations with mypy
- Google/NumPy style docstrings
- PascalCase for classes, snake_case for functions/variables

## Error Handling
- Use hierarchy of exceptions extending from `A2AError` base class
- Catch specific exceptions (e.g., `A2AConnectionError`) rather than generic ones
- Provide descriptive error messages

## Project Structure
- Modular organization with clients, servers, models, and utils
- Tests in `/tests` directory using pytest
- Examples demonstrating different use cases in `/examples`
- Extensive type annotations throughout

## Example Standards
- All examples should have descriptive docstrings explaining their purpose
- Examples should be able to run independently with minimal setup
- Examples requiring API keys should support a `--test-mode` flag for validation
- When `--test-mode` is used, examples should create mock components that don't need API calls
- Examples that start servers should support the `--port` argument for port configuration
- Add proper error handling for clean exit during validation

## Validation Script Maintenance
- When adding new examples, update `examples/validate_all_examples.py` to include them
- Each example in the validation script should include:
  - Required arguments for automated testing
  - Success markers that indicate successful execution
  - Appropriate timeout settings
  - API key requirements (if any)
  - Test mode support for categories like `langchain` and `ai_powered_agents`
- Categories that require API keys should have consistent handling in the validation script
- The validation script should detect real API keys and use them when available instead of mocks
- Keep output styles consistent between similar categories (e.g., langchain and ai_powered_agents)