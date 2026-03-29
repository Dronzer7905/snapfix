/**
 * snapfix/src/tracebackDetector.ts
 *
 * Author: Snapfix Contributors
 * License: MIT
 *
 * TracebackDetector: a stateful line-buffer state machine that accumulates
 * terminal output chunks and emits a complete traceback string once the
 * error line is detected.
 */

type DetectorState = "IDLE" | "COLLECTING" | "COMPLETE";

const TRACEBACK_HEADER = "Traceback (most recent call last):";
const FRAME_START_RE = /^\s+File "(.+)", line (\d+)/;
const ERROR_LINE_RE = /^([A-Z][A-Za-z0-9_.]*(?:Error|Exception|Warning|Interrupt|Exit|Fault|Stop|DoesNotExist|GeneratorExit|KeyboardInterrupt|SystemExit))\s*:\s*.+$/;

export class TracebackDetector {
  private _state: DetectorState = "IDLE";
  private _buffer: string[] = [];
  private _partial: string = "";

  public feed(chunk: string): string | null {
    const text = this._partial + chunk;
    const rawLines = text.split("\n");
    this._partial = rawLines.pop() ?? "";

    for (const rawLine of rawLines) {
      const line = stripAnsi(rawLine);
      const result = this._processLine(line);
      if (result !== null) return result;
    }
    return null;
  }

  public reset(): void {
    this._state = "IDLE";
    this._buffer = [];
    this._partial = "";
  }

  private _processLine(line: string): string | null {
    switch (this._state) {
      case "IDLE":
        if (line.includes(TRACEBACK_HEADER) || FRAME_START_RE.test(line)) {
          this._state = "COLLECTING";
          this._buffer = [line];
        }
        return null;

      case "COLLECTING":
        this._buffer.push(line);
        if (ERROR_LINE_RE.test(line.trim())) {
          this._state = "COMPLETE";
          return this._flush();
        }
        if (this._buffer.length > 200) this.reset();
        return null;

      case "COMPLETE":
        return null;
    }
  }

  private _flush(): string {
    const result = this._buffer.join("\n");
    this.reset();
    return result;
  }
}

function stripAnsi(text: string): string {
  // eslint-disable-next-line no-control-regex
  return text.replace(/\x1B\[[0-9;]*[mGKHFJABCDEFhilmnprsu]|\x1B\][^\x07]*\x07|\x1B\[[^a-z]*[a-z]/gi, "");
}
