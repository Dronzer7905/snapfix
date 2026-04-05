# Snapfix — VS Code Extension

<p align="left">
  <strong>Real-time Python traceback analysis directly inside VS Code.</strong> 🧠
</p>

The **Snapfix Extension** intelligently watches your integrated VS Code terminal for Python exceptions. The moment a crash occurs, it hooks into the [Snapfix Engine](https://github.com/Dronzer7905/snapfix/tree/main/snapfix-backend) automatically, bringing an elegantly designed side panel into view. It explains the error in plain English and provides the exact code needed to fix it.

No more copying and pasting stack traces into chat windows. 

---

## 🛠️ Requirements & Prerequisites

To unlock this seamless developer experience, you must have the following installed:

- **VS Code** Version 1.85 or higher.
- **Python** 3.10+ (to run the companion Python backend server).
- **Node.js** (Only if building the extension manually from source).
- [Optional but Recommended] **Ollama** running locally (if you want 100% private, free, on-device analysis).

---

## 📥 Installation

> [!NOTE]
> Until the extension is publicly published to the VS Code Marketplace, you must compile it from source as a standard `.vsix` file.

### Step 1: Install the Backend Engine
The extension requires the Python library to perform the analysis. Open your terminal:
```bash
python -m pip install -e "git+https://github.com/Dronzer7905/snapfix.git#egg=snapfix&subdirectory=snapfix-backend"
```
*(Alternatively, clone the repository and run `python -m pip install -e .` inside `snapfix-backend`)*

### Step 2: Build the Extension
Next, package the TypeScript frontend:
```bash
git clone https://github.com/Dronzer7905/snapfix.git
cd snapfix/snapfix-vscode
npm install
npm run package
```

### Step 3: Install the VSIX
1. Open VS Code.
2. Go to the **Extensions view** (`Ctrl+Shift+X` or `Cmd+Shift+X`).
3. Click the explicit `...` completely in the upper right. 
4. Select **"Install from VSIX..."** from the dropdown menu.
5. Browse to the `snapfix-vscode` folder and select the `snapfix-vscode-0.1.0.vsix` file.

Now, simply open any Python project and try throwing an error in the terminal!

---

## ⚙️ Extension Settings

Snapfix aims for a zero-config onboarding workflow. However, you can deeply customize its behavior via your VS Code Settings JSON (`settings.json`).

| Configuration Key | Default | Description |
| :--- | :--- | :--- |
| `snapfix.serverPort` | `7842` | The port the Python backend server is instructed to listen on. |
| `snapfix.serverHost` | `127.0.0.1` | The host interface the server binds to. |
| `snapfix.autoAnalyze` | `true` | If true, the side panel pops open instantly upon a traceback. |
| `snapfix.pythonPath` | `python` | The Python executable used to spawn the background backend server. |

---

## ⌨️ Command Palette Utilities

Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to access these core Snapfix commands:

| Command | Action Performed |
| :--- | :--- |
| **`Snapfix: Show Analysis Panel`** | Manually opens or focuses the analysis side panel webview. |
| **`Snapfix: Restart Analysis Server`** | Forcefully kills and respawns the hidden Python background server. Useful if the connection drops. |
| **`Snapfix: Clear Analysis Cache`** | Wipes all previously cached LLM lookups locally from the SQLite database. |

---

## 📄 License & Attribution

Open-sourced specifically under the **MIT License**.
© [Snapfix Contributors](https://github.com/Dronzer7905/snapfix/graphs/contributors)
