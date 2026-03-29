# PyLogAI — VS Code Extension

> Real-time Python traceback analysis in a VS Code side panel, powered by [PyLogAI](https://github.com/pylogai/pylogai).

---

## Requirements

- VS Code 1.85+
- Python 3.10+ with `pylogai` installed (`pip install pylogai`)
- [Ollama](https://ollama.com) running locally (default) **or** an OpenAI / Anthropic API key

## Installation

1. Install from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=pylogai.pylogai)
2. Install the Python server: `pip install pylogai`
3. Pull an Ollama model: `ollama pull llama3.2`
4. Open a Python project and run your code — error analysis appears automatically

---

## Extension Settings

| Setting | Default | Description |
|---|---|---|
| `pylogai.serverPort` | `7842` | Port the PyLogAI server listens on |
| `pylogai.serverHost` | `127.0.0.1` | Host the server binds to |
| `pylogai.autoAnalyze` | `true` | Auto-analyze tracebacks as they appear |
| `pylogai.pythonPath` | `python` | Python executable to spawn the server |

---

## Commands

| Command | Description |
|---|---|
| `PyLogAI: Show Analysis Panel` | Open / focus the side panel |
| `PyLogAI: Restart Analysis Server` | Kill and respawn the Python server |
| `PyLogAI: Clear Analysis Cache` | Wipe all cached analyses |

---

## CHANGELOG

### 0.1.0
- Initial release
- Terminal watcher with per-terminal TracebackDetector state machine
- Auto-spawns PyLogAI Python server on VS Code startup
- Side panel with error card, explanation, fix, and docs link
- Supports Ollama (default), OpenAI, Anthropic via `config.toml`
- Local SQLite cache for instant repeat lookups

---

## License

MIT © [PyLogAI Contributors](https://github.com/pylogai/pylogai-vscode/graphs/contributors)
