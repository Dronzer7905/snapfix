<div align="center">
  <img src="https://raw.githubusercontent.com/Dronzer7905/snapfix/main/assets/logo.png" alt="Snapfix Logo" width="120" />
</div>

<h1 align="center">Snapfix</h1>

<p align="center">
  <strong>🔥 Premium AI-Powered Python Error Analysis Engine 🔥</strong>
</p>

<p align="center">
  <a href="#-why-snapfix">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## 🚀 Overview

**Snapfix** is an advanced, AI-driven error analysis ecosystem designed to transform raw, cryptic Python tracebacks into clean, actionable, and developer-friendly reports. It embeds directly into your workflow, providing instant context, plain-English explanations, and copy-pasteable fixes.

No more copying errors to ChatGPT. Snapfix brings the AI directly to your editor seamlessly.

### 🌟 Why Snapfix?

- **⚡ Instant Context**: Detects and analyzes tracebacks from your terminal in real-time.
- **🧠 Intelligent Explanations**: Understands the underlying cause and explains it simply.
- **🛠️ Actionable Solutions**: Generates exact Python fixes (with inline `# snapfix:` comments).
- **🛡️ Proactive Prevention**: Provides tips on code quality to prevent bugs before they happen.
- **🔒 Privacy First**: Designed to run 100% locally using **Ollama** by default. Your code never leaves your machine unless you explicitly configure a cloud provider (like OpenAI or Gemini).

---

## 📦 System Architecture

Snapfix is composed of two seamlessly integrated parts:

1. **[Snapfix Engine (Backend)](./snapfix-backend)**: A high-performance Python server. It manages traceback parsing, communicates with LLMs (via LiteLLM), and caches results locally in SQLite for lightning-fast repeat analysis.
2. **[Snapfix VS Code Extension](./snapfix-vscode)**: A premium developer interface. It watches your terminal for exceptions, parses them automatically, and surfaces the AI analysis in a beautifully designed side panel within VS Code.

---

## ⚡ Quick Start

Follow these simple steps to get the Snapfix ecosystem running locally on your machine.

> [!NOTE]
> Prerequisites: Ensure you have **Python 3.10+** and **Node.js** installed on your system.

### Step 1: Install the Backend Engine

The backend handles all the heavy lifting for error analysis.

```bash
# 1. Navigate to the backend directory
cd snapfix-backend

# 2. Install the engine locally
python -m pip install -e .

# 3. Start the Snapfix server
python -m snapfix server
```

> [!TIP]
> The server typically starts on `http://127.0.0.1:7842`. On first launch, it will auto-generate a configuration file at `~/.snapfix/config.toml` where you can set your preferred AI model (e.g., local Ollama, or an API key for Gemini/OpenAI).

### Step 2: Install the VS Code Extension

The extension acts as the bridge between your code and the analysis engine.

```bash
# 1. Navigate to the extension folder
cd snapfix-vscode

# 2. Install dependencies
npm install

# 3. Package the extension into a standard .vsix installer
npm run package
```

4. Once packaged, you will see a `.vsix` file in the directory. Install this into VS Code:
   - Go to the **Extensions** view (`Ctrl+Shift+X` or `Cmd+Shift+X`).
   - Click the `...` menu in the top right of the extensions pane and select **Install from VSIX**.
   - Browse to and select the generated `.vsix` file.
   - Restart VS Code if prompted. You're now ready to use Snapfix!

---

## 🤝 Call for Contributors!

**We are actively inviting collaborators!** Whether you're a seasoned Python backend engineer, an AI prompt-engineering enthusiast, or a frontend wizard looking to improve our VS Code extension UI, there's a vital place for you here.

> [!IMPORTANT]
> This project is growing fast, and we value every single contribution—from raising issues to submitting major feature pull requests. Let's build the ultimate developer tool together. 🚀

Ready to jump in? Check out our official **[Contribution Guide](./CONTRIBUTING.md)** for a complete, step-by-step walkthrough on setting up your dev environment, our architecture rules, and how to open your first Pull Request. 

Please ensure you review our **[Code of Conduct](./CODE_OF_CONDUCT.md)** to help us maintain a safe, welcoming, and professional community.

---

## 📄 License

This project is open-source and licensed under the **MIT License**. Check the [LICENSE](./LICENSE) file for full details.

<p align="center">Made with ❤️ by <a href="https://github.com/Dronzer7905">Dronzer7905</a> and contributors.</p>
