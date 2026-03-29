# Changelog

All notable changes to the PyLogAI VS Code extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-03-17

### Added
- Initial release of PyLogAI VS Code extension.
- **TerminalWatcher**: Hooks into terminal data to detect Python tracebacks.
- **TracebackDetector**: State machine for robust multi-chunk traceback detection.
- **SidePanel**: Rich webview for displaying AI-powered explanations and fixes.
- **ServerManager**: Automatic lifecycle management of the `pylogai` Python server.
- **Cache Support**: Local SQLite caching for near-instant repeat lookups.
- **Multi-provider Support**: Works with Ollama (default), OpenAI, and Anthropic.
