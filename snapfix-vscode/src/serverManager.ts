/**
 * snapfix/src/serverManager.ts
 *
 * Author: Snapfix Contributors
 * License: MIT
 */

import * as cp from "child_process";
import * as http from "http";
import * as vscode from "vscode";

export interface ServerManagerOptions {
  host: string;
  port: number;
  pythonPath: string;
  workspaceRoot?: string;
}

const MAX_HEALTH_RETRIES = 15;
const HEALTH_RETRY_DELAY_MS = 1000;

export class ServerManager implements vscode.Disposable {
  private readonly _options: ServerManagerOptions;
  private _process: cp.ChildProcess | null = null;

  constructor(options: ServerManagerOptions) {
    this._options = options;
  }

  public async ensureRunning(): Promise<void> {
    const running = await this._isHealthy();
    if (running) return;

    const python = await this._getEffectivePythonPath();
    const installed = await this._checkSnapfixInstalled(python);

    if (!installed) {
      const choice = await vscode.window.showErrorMessage(
        "Snapfix: The `snapfix` backend is not installed in your Python environment.",
        "Install Now",
        "Settings"
      );
      if (choice === "Install Now") {
        await this._installBackend(python);
      } else if (choice === "Settings") {
        vscode.commands.executeCommand("workbench.action.openSettings", "snapfix.pythonPath");
        return;
      } else {
        return;
      }
    }

    this._spawn(python);
    await this._waitForHealthy();
  }

  public async restart(): Promise<void> {
    this._kill();
    const python = await this._getEffectivePythonPath();
    this._spawn(python);
    await this._waitForHealthy();
  }

  public dispose(): void {
    this._kill();
  }

  private _spawn(pythonPath: string): void {
    const { host, port } = this._options;
    const args = ["-m", "snapfix", "server", "--host", host, "--port", String(port)];

    this._process = cp.spawn(pythonPath, args, {
      detached: false,
      shell: false,
      stdio: ["ignore", "pipe", "pipe"],
    });

    this._process.stdout?.on("data", (chunk: Buffer) => {
      console.log("[snapfix-server]", chunk.toString().trim());
    });

    this._process.stderr?.on("data", (chunk: Buffer) => {
      console.error("[snapfix-server]", chunk.toString().trim());
    });

    this._process.on("exit", (code) => {
      if (code !== 0 && code !== null && !this._process?.killed) {
        vscode.window.showWarningMessage(`Snapfix Engine exited with code ${code}. Run "Snapfix: Restart Server" to try again.`);
      }
    });

    this._process.on("error", (err) => {
      vscode.window.showErrorMessage(`Snapfix: failed to start server: ${err.message}.`);
    });
  }

  private async _getEffectivePythonPath(): Promise<string> {
    const { pythonPath, workspaceRoot } = this._options;
    if (pythonPath && pythonPath !== "python" && pythonPath !== "python3") {
      if (await this._pathExists(pythonPath)) return pythonPath;
    }

    if (workspaceRoot) {
      const fs = require("fs");
      const path = require("path");
      const venvPatterns = [
        ["venv", "Scripts", "python.exe"],
        [".venv", "Scripts", "python.exe"],
        ["venv", "bin", "python"],
        [".venv", "bin", "python"],
      ];

      for (const pattern of venvPatterns) {
        const fullPath = path.join(workspaceRoot, ...pattern);
        if (fs.existsSync(fullPath)) return fullPath;
      }
    }
    return pythonPath || "python";
  }

  private async _checkSnapfixInstalled(pythonPath: string): Promise<boolean> {
    return new Promise((resolve) => {
      // Check for snapfix
      cp.exec(`"${pythonPath}" -m snapfix --help`, (err) => {
        resolve(!err);
      });
    });
  }

  private async _installBackend(pythonPath: string): Promise<void> {
    const terminal = vscode.window.createTerminal("Snapfix Installer");
    terminal.show();
    
    const path = require("path");
    const fs = require("fs");
    // Path to the local snapfix packge
    const localSnapfix = this._options.workspaceRoot ? path.join(this._options.workspaceRoot, "pylogai") : null;

    if (localSnapfix && fs.existsSync(localSnapfix)) {
      terminal.sendText(`"${pythonPath}" -m pip install -e "${localSnapfix}"`);
    } else {
      terminal.sendText(`"${pythonPath}" -m pip install snapfix`);
    }

    vscode.window.showInformationMessage("Snapfix: Installing backend... Please wait.");
  }

  private _pathExists(p: string): Promise<boolean> {
    const fs = require("fs");
    return Promise.resolve(fs.existsSync(p));
  }

  private _kill(): void {
    if (this._process && !this._process.killed) {
      this._process.kill("SIGTERM");
      this._process = null;
    }
  }

  private _isHealthy(): Promise<boolean> {
    const { host, port } = this._options;
    return new Promise((resolve) => {
      const req = http.get({ hostname: host, port, path: "/health", timeout: 1500 }, (res) => resolve(res.statusCode === 200));
      req.on("error", () => resolve(false));
      req.on("timeout", () => {
        req.destroy();
        resolve(false);
      });
      req.end();
    });
  }

  private async _waitForHealthy(): Promise<void> {
    for (let i = 0; i < MAX_HEALTH_RETRIES; i++) {
      await new Promise(r => setTimeout(r, HEALTH_RETRY_DELAY_MS));
      if (await this._isHealthy()) return;
    }
    vscode.window.showErrorMessage("Snapfix: server did not start in time. Check installation.");
  }
}
