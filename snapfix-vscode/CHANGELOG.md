# Changelog

All notable changes to the **Snapfix VS Code Extension** will be explicitly documented in this file.

The precise format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project strongly adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-03-31 (Current Release)

This release marks the transition from the experimental "PyLogAI" internal name to the premium, unified **Snapfix Ecosystem**. It includes major UI overhauls, more robust error caching, and a vastly improved onboard server deployment process.

### Added
- **Total Workspace Integration**: Initial public release of the newly branded Snapfix VS Code extension.
- **TerminalWatcher Core**: Hooks deeply into terminal outputs via `vscode.window.onDidWriteTerminalData` to instantly detect active Python stack trace emissions.
- **TracebackDetector**: A highly resilient state machine engineered specifically for robust, multi-chunk, cross-platform traceback compilation.
- **Snapfix Panel**: A visually stunning Webview implementing a modern, Glassmorphism-inspired UI tailored for displaying AI-generated plain-English explanations and precise code copy/paste functionality.
- **Background Daemon Management**: Implemented an automated lifecycle manager that quietly boots the Snapfix Python REST server implicitly on VS Code startup.
- **Database Caching Protocol**: Uses an asynchronous SQLite layer directly to provide lightning-fast (near-instantaneous) repeat lookups without exhausting local hardware limits.

### Changed
- **Massive Rebranding**: All user-facing components updated globally from `PyLogAI` to `Snapfix`. 
- **Prompt Engineering**: Substantially refined the underlying LLM system prompt instructing models to format code natively for the React webview layer using `# snapfix:` commented structure protocols.

### Supported Integrations
- Shipped primarily out of the box with `ollama/llama3.2` logic (100% private caching enabled).
- Fully supports OpenAI (`gpt-4-turbo`), Anthropic (`claude-3-opus`), and generic LiteLLM proxy interfaces through explicit custom definitions in `config.toml`.
