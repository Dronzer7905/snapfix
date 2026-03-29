/**
 * snapfix/src/sidePanel.ts
 *
 * Author: Snapfix Contributors
 * License: MIT
 */

import * as vscode from "vscode";
import type { AnalyzeResponse } from "./httpClient";

export class SidePanelManager {
  private _panel: vscode.WebviewPanel | null = null;
  private readonly _extensionUri: vscode.Uri;

  constructor(extensionUri: vscode.Uri) {
    this._extensionUri = extensionUri;
  }

  public show(response: AnalyzeResponse | null): void {
    if (this._panel) {
      this._panel.reveal(vscode.ViewColumn.Two);
    } else {
      this._panel = vscode.window.createWebviewPanel(
        "snapfix.panel",
        "Snapfix Engine — Analysis",
        vscode.ViewColumn.Two,
        {
          enableScripts: true,
          localResourceRoots: [vscode.Uri.joinPath(this._extensionUri, "webview")],
          retainContextWhenHidden: true,
        }
      );

      this._panel.onDidDispose(() => {
        this._panel = null;
      });
    }

    this._panel.webview.html = this._buildHtml(response);
  }

  private _buildHtml(response: AnalyzeResponse | null): string {
    if (!response) return this._welcomeHtml();

    const { what_happened, fix, stack_frames, prevention, docs, meta, cached } = response;
    
    // Severity color
    const severityColor = meta.severity === "high" ? "#FF5A5A" : (meta.severity === "medium" ? "#F5A623" : "#00C896");
    const confidencePrefix = meta.confidence === "low" ? "?" : (meta.confidence === "medium" ? "~" : "");

    // Format stack trace rows
    const stackTraceHtml = stack_frames.map(f => `
      <div class="p-2 border-l ${f.is_origin ? 'border-snap bg-[#0D1008]' : 'border-border-dim opacity-50'}">
        <div class="font-mono text-[10px] ${f.is_origin ? 'text-snap' : 'text-mist'}">${escapeHtml(f.file)}:${f.line}</div>
        <div class="font-mono text-[11px] ${f.is_origin ? 'text-text-1' : ''}">${escapeHtml(f.function)}</div>
        <div class="font-mono text-[10px] mt-1 opacity-70">${escapeHtml(f.snippet)}</div>
      </div>
    `).join("");

    return /* html */ `
<!DOCTYPE html>
<html class="dark" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Snapfix Engine</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "ink": "#0B0E14",
                        "surface": "#141820",
                        "border-dim": "#1E2530",
                        "snap": "#00C896",
                        "err": "#FF5A5A",
                        "warn": "#F5A623",
                        "mist": "#85948c",
                        "text-1": "#e1e2eb",
                        "text-2": "#bbcac1",
                        "text-3": "#3E4E5A",
                        "primary": "#42e5b0",
                        "background": "#0B0E14"
                    },
                    fontFamily: {
                        "headline": ["Space Grotesk", "sans-serif"],
                        "mono": ["JetBrains Mono", "monospace"],
                        "body": ["DM Sans", "sans-serif"]
                    },
                    borderRadius: { "DEFAULT": "0px" }
                }
            }
        }
    </script>
    <style>
        .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 20; font-size: 18px; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #0B0E14; }
        ::-webkit-scrollbar-thumb { background: #1E2530; }
        .pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .4; } }
        body { min-height: 100vh; overflow-y: auto; }
    </style>
</head>
<body class="bg-ink text-text-1 font-body selection:bg-snap selection:text-ink overflow-x-hidden flex flex-col p-0 m-0">
<header class="fixed top-0 w-full border-b border-[#1E2530] z-50 flex items-center justify-between px-3 h-10 bg-[#0B0E14]">
    <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-[#00C896]">menu_open</span>
        <h1 class="text-[#00C896] font-['JetBrains_Mono'] font-bold text-lg tracking-widest uppercase">
            <span class="text-white">Snap</span>fix
        </h1>
    </div>
</header>
<main class="flex-1 mt-10 mb-6 overflow-y-auto border-x border-border-dim">
    <section class="p-4 border-b border-border-dim bg-surface/30" style="border-left: 4px solid ${severityColor}">
        <div class="flex items-center justify-between mb-2">
            <span class="font-mono text-[${severityColor}] font-bold text-xs tracking-tighter uppercase">${meta.category}</span>
            <div class="flex gap-1">
                ${meta.framework_hint ? `<span class="bg-snap/10 text-snap px-1.5 py-0.5 text-[9px] font-mono border border-snap/20 uppercase">${meta.framework_hint}</span>` : ''}
                <span class="bg-snap/10 text-snap px-1.5 py-0.5 text-[9px] font-mono border border-snap/20 uppercase">${confidencePrefix}${cached ? 'Cached' : 'AI'}</span>
            </div>
        </div>
        <h2 class="font-mono text-sm leading-tight text-text-1 break-words">${escapeHtml(what_happened.headline)}</h2>
    </section>
    
    <section class="border-b border-border-dim">
        <button class="w-full flex items-center justify-between p-3" onclick="toggleAccordion('analysis')">
            <span class="text-[11px] font-bold uppercase tracking-widest text-text-3">Analysis</span>
            <span class="material-symbols-outlined text-text-3" id="analysis-icon">expand_more</span>
        </button>
        <div class="p-3 pt-0 text-sm text-text-2 leading-relaxed" id="analysis">
            ${escapeHtml(what_happened.detail)}
        </div>
    </section>

    <section class="p-4 border-b border-border-dim">
        <div class="flex items-center justify-between mb-3">
            <span class="text-[11px] font-bold uppercase tracking-widest text-text-3">Suggested Fix</span>
            <button class="text-[10px] font-mono text-snap hover:underline" onclick="copyCode(this)">COPY_CODE</button>
        </div>
        <div class="bg-surface border border-border-dim p-3 font-mono text-xs mb-3 overflow-x-auto">
            <pre class="text-text-2"><code>${escapeHtml(fix.code)}</code></pre>
        </div>
        <p class="text-[11px] text-text-3 mb-3">${escapeHtml(fix.explanation)}</p>
    </section>

    <section class="border-b border-border-dim">
        <button class="w-full flex items-center justify-between p-3" onclick="toggleAccordion('trace')">
            <span class="text-[11px] font-bold uppercase tracking-widest text-text-3">Stack Trace</span>
            <span class="material-symbols-outlined text-text-3" id="trace-icon">expand_more</span>
        </button>
        <div class="px-3 pb-4 space-y-2" id="trace">
            ${stackTraceHtml}
        </div>
    </section>

    <section class="p-4 border-b border-border-dim">
        <div class="flex gap-3 bg-surface p-3 border-l-2 border-warn">
            <span class="material-symbols-outlined text-warn">info</span>
            <div class="text-[12px] text-text-2 leading-snug">
                <span class="text-text-1 font-bold">Pro-tip:</span> ${escapeHtml(prevention.tip)}
                ${prevention.pattern ? `<div class="mt-2 font-mono text-[10px] bg-ink/50 p-2">${escapeHtml(prevention.pattern)}</div>` : ''}
            </div>
        </div>
    </section>

    <section class="p-4">
        <a class="flex items-center gap-2 text-[11px] font-mono text-text-3 hover:text-snap transition-colors" href="${escapeHtml(docs.url)}">
            <span class="material-symbols-outlined text-[14px]">link</span>
            ${escapeHtml(docs.label)}
            <span class="material-symbols-outlined text-[12px]">open_in_new</span>
        </a>
    </section>
</main>
<footer class="fixed bottom-0 w-full z-50 flex items-center justify-between px-2 text-[10px] bg-[#141820] border-t border-[#1E2530] h-6 font-mono">
    <div class="flex items-center gap-1.5 text-[#3E4E5A]">
        <span class="w-1.5 h-1.5 bg-snap rounded-full pulse"></span>
        <span>watching terminal</span>
    </div>
    <div class="flex items-center gap-1.5 text-[#3E4E5A]">
        <span class="text-[#00C896]">model: ${confidencePrefix}active</span>
    </div>
</footer>
<script>
    function toggleAccordion(id) {
        const el = document.getElementById(id);
        const icon = document.getElementById(id + '-icon');
        el.classList.toggle('hidden');
        icon.innerText = el.classList.contains('hidden') ? 'chevron_right' : 'expand_more';
    }
    function copyCode(btn) {
        const code = btn.closest('section').querySelector('code').innerText;
        navigator.clipboard.writeText(code).then(() => {
            const original = btn.innerText;
            btn.innerText = 'COPIED_✓';
            setTimeout(() => btn.innerText = original, 2000);
        });
    }
</script>
</body>
</html>
`;
  }

  private _welcomeHtml(): string {
    return `
<!DOCTYPE html>
<html class="dark" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0B0E14; color: #85948c; font-family: sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; }
        .logo { color: #00C896; font-size: 24px; font-weight: bold; letter-spacing: 2px; margin-bottom: 20px; }
        .text { max-width: 300px; line-height: 1.5; font-size: 13px; }
    </style>
</head>
<body>
    <div>
        <div class="logo">SNAPFIX</div>
        <div class="text">
            Run your Python code. When an error occurs, Snapfix will automatically analyze the traceback and suggest a fix here.
        </div>
    </div>
</body>
</html>
`;
  }
}

function escapeHtml(str: string): string {
  if (!str) return "";
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}
