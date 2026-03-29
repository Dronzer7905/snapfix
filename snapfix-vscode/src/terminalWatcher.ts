/**
 * snapfix/src/terminalWatcher.ts
 *
 * Author: Snapfix Contributors
 * License: MIT
 */

import * as vscode from "vscode";
import type { HttpClient } from "./httpClient";
import type { SidePanelManager } from "./sidePanel";
import { TracebackDetector } from "./tracebackDetector";

export class TerminalWatcher {
  private readonly _http: HttpClient;
  private readonly _panel: SidePanelManager;
  private readonly _detectors = new Map<string, TracebackDetector>();

  constructor(http: HttpClient, panel: SidePanelManager) {
    this._http = http;
    this._panel = panel;
  }

  public register(): vscode.Disposable {
    const sub = (vscode.window as any).onDidWriteTerminalData(
      this._onData.bind(this)
    );

    const closeSub = vscode.window.onDidCloseTerminal((terminal) => {
      void terminal.processId.then((pid: number | undefined) => {
        if (pid !== undefined) {
          this._detectors.delete(String(pid));
        }
      });
    });

    return vscode.Disposable.from(sub, closeSub);
  }

  private _onData(event: any): void {
    void event.terminal.processId.then((pid: number | undefined) => {
      const key = String(pid ?? "unknown");
      if (!this._detectors.has(key)) {
        this._detectors.set(key, new TracebackDetector());
      }
      const detector = this._detectors.get(key)!;
      const traceback = detector.feed(event.data);
      if (traceback !== null) {
        vscode.window.showInformationMessage("Snapfix: Traceback detected! Analyzing...");
        void this._analyze(traceback);
      }
    });
  }

  private async _analyze(traceback: string): Promise<void> {
    const config = vscode.workspace.getConfiguration("snapfix");
    const autoAnalyze = config.get<boolean>("autoAnalyze", true);
    if (!autoAnalyze) {
      return;
    }

    try {
      const response = await this._http.analyze({
        traceback,
        context: "python",
        session_id: vscode.env.sessionId,
        project_path: vscode.workspace.workspaceFolders?.[0].uri.fsPath ?? "",
      });
      this._panel.show(response);
    } catch (err: any) {
      const msg = err.message || String(err);
      vscode.window.showErrorMessage(`Snapfix analysis failed: ${msg}`);
    }
  }
}
