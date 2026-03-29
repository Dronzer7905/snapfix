/**
 * snapfix/src/httpClient.ts
 *
 * Author: Snapfix Contributors
 * License: MIT
 */

import * as http from "http";

export interface AnalyzeRequest {
  traceback: string;
  context: string;
  session_id?: string;
  project_path?: string;
}

export interface AnalyzeResponse {
  what_happened: {
    headline: string;
    detail: string;
  };
  fix: {
    explanation: string;
    code: string;
    language: string;
  };
  stack_frames: Array<{
    file: string;
    line: number;
    function: string;
    snippet: string;
    is_origin: boolean;
  }>;
  prevention: {
    tip: string;
    pattern: string;
  };
  docs: {
    label: string;
    url: string;
  };
  meta: {
    severity: "low" | "medium" | "high";
    category: string;
    framework_hint: string;
    confidence: "high" | "medium" | "low";
  };
  cached: boolean;
}

export interface HttpClientOptions {
  host: string;
  port: number;
  timeoutMs?: number;
}

const DEFAULT_TIMEOUT_MS = 60_000;

export class HttpClient {
  private readonly _host: string;
  private readonly _port: number;
  private readonly _timeoutMs: number;

  constructor(options: HttpClientOptions) {
    this._host = options.host;
    this._port = options.port;
    this._timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  }

  public analyze(payload: AnalyzeRequest): Promise<AnalyzeResponse> {
    return this._post<AnalyzeResponse>("/analyze", payload);
  }

  public clearCache(): Promise<boolean> {
    return this._post<{ success: boolean }>("/cache/clear", {}).then(r => r.success);
  }

  public health(): Promise<boolean> {
    return new Promise((resolve) => {
      const options: http.RequestOptions = {
        hostname: this._host,
        port: this._port,
        path: "/health",
        method: "GET",
        timeout: 2000,
      };
      const req = http.request(options, (res) => resolve(res.statusCode === 200));
      req.on("error", () => resolve(false));
      req.on("timeout", () => {
        req.destroy();
        resolve(false);
      });
      req.end();
    });
  }

  private _post<T>(path: string, body: unknown): Promise<T> {
    const json = JSON.stringify(body);
    const options: http.RequestOptions = {
      hostname: this._host,
      port: this._port,
      path,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(json),
      },
      timeout: this._timeoutMs,
    };

    return new Promise<T>((resolve, reject) => {
      const req = http.request(options, (res) => {
        const chunks: any[] = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          const raw = Buffer.concat(chunks).toString("utf8");
          if (res.statusCode && res.statusCode >= 400) {
            reject(new Error(`Snapfix Engine error ${res.statusCode}: ${raw}`));
            return;
          }
          try {
            resolve(JSON.parse(raw) as T);
          } catch {
            reject(new Error(`Invalid JSON from Snapfix Engine: ${raw}`));
          }
        });
      });

      req.on("error", (err) => reject(err));
      req.on("timeout", () => {
        req.destroy();
        reject(new Error("Snapfix Engine request timed out"));
      });

      req.write(json);
      req.end();
    });
  }
}
