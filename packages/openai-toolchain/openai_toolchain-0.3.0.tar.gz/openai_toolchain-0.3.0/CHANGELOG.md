# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2025-05-26

### Added

- Added support for non-AI parameters in `@tool` decorator
- New `tool_params` parameter in `chat_with_tools` for passing non-AI parameters
- Documentation and examples for using non-AI parameters

## [0.2.0] - 2025-05-23

### Removed

- Compatibility for Python versions before 3.10

## [0.1.0] - 2025-05-22

### Added

- Initial release of OpenAI Toolchain
- Core functionality for registering and managing OpenAI function tools
- `OpenAIClient` class for simplified interaction with OpenAI's API
- `@tool` decorator for easy function registration
- Support for automatic tool calling and response handling
