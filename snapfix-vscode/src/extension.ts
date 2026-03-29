/**
 * snapfix/src/extension.ts
 *
 * Author: Snapfix Contributors
 * License: MIT
 */

import * as vscode from "vscode";
import { HttpClient } from "./httpClient";
import { ServerManager } from "./serverManager";
import { SidePanelManager } from "./sidePanel";
import { TerminalWatcher } from "./terminalWatcher";

const disposables: vscode.Disposable[] = [];

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  const config = vscode.workspace.getConfiguration("snapfix");

  const host: string = config.get<string>("serverHost", "127.0.0.1");
  const port: number = config.get<number>("serverPort", 7842);
  const pythonPath: string = config.get<string>("pythonPath", "python");

  const serverManager = new ServerManager({
    host,
    port,
    pythonPath,
    workspaceRoot: vscode.workspace.workspaceFolders?.[0].uri.fsPath,
  });
  const httpClient = new HttpClient({ host, port });
  const sidePanelManager = new SidePanelManager(context.extensionUri);
  const terminalWatcher = new TerminalWatcher(httpClient, sidePanelManager);

  void serverManager.ensureRunning();

  disposables.push(
    vscode.commands.registerCommand("snapfix.showPanel", () => {
      sidePanelManager.show(null);
    })
  );

  disposables.push(
    vscode.commands.registerCommand("snapfix.restartServer", async () => {
      await serverManager.restart();
      vscode.window.showInformationMessage("Snapfix Engine restarted.");
    })
  );

  disposables.push(
    vscode.commands.registerCommand("snapfix.analyzeClipboard", async () => {
      const clipboardText = await vscode.env.clipboard.readText();
      if (!clipboardText || clipboardText.trim().length < 10) {
        vscode.window.showWarningMessage("Snapfix: Please copy a traceback to the clipboard first.");
        return;
      }
      vscode.window.showInformationMessage("Snapfix: analyzing clipboard traceback...");
      try {
        const response = await httpClient.analyze({
          traceback: clipboardText,
          context: "python",
          session_id: vscode.env.sessionId,
          project_path: vscode.workspace.workspaceFolders?.[0].uri.fsPath ?? "",
        });
        sidePanelManager.show(response);
      } catch (err: any) {
        vscode.window.showErrorMessage(`Snapfix: analysis failed: ${err.message}`);
      }
    })
  );

  disposables.push(
    vscode.commands.registerCommand("snapfix.clearCache", async () => {
      vscode.window.showInformationMessage("Snapfix: clearing cache...");
      try {
        await httpClient.clearCache();
        vscode.window.showInformationMessage("Snapfix: cache cleared.");
      } catch (err: any) {
        vscode.window.showErrorMessage(`Snapfix: failed to clear cache: ${err.message}`);
      }
    })
  );

  disposables.push(terminalWatcher.register());
  context.subscriptions.push(...disposables);
}

export function deactivate(): void {
  for (const d of disposables) {
    d.dispose();
  }
  disposables.length = 0;
}
