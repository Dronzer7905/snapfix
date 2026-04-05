# 🛡️ Snapfix Security Policy

Security is a primary concern for the **Snapfix** ecosystem, especially because we handle sensitive developer environment data, code snippets, and tracebacks. We greatly appreciate the efforts of security researchers and our community in responsibly disclosing vulnerabilities to us.

---

## ✅ Supported Versions

We recommend all users stay on the latest minor release for maximum stability and security. The following major/minor versions of Snapfix are currently actively supported with security updates.

| Version | Status | Notes |
| :---: | :---: | :--- |
| **0.2.x** | 🟩 Supported | Active development & patches |
| **0.1.x** | 🟧 Limited | Critical security patches only |
| **< 0.1.0** | 🟥 Unsupported | Please upgrade immediately |

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability within the Snapfix Engine (backend) or the VS Code Extension, **please do not open a public GitHub issue**. We ask that you follow a coordinated disclosure process to keep our users safe.

### How to Report

1.  **Email Us:** Send a detailed report to our dedicated security inbox: **[security@dronzer.me]**
2.  **Wait for Acknowledgement:** Please allow our maintainers up to **48 hours** to acknowledge receipt of your report.
3.  **Triage & Fix:** We will actively investigate the issue, determine its severity, and coordinate a patch internally. We may request further details from you during this stage.
4.  **Coordinated Disclosure:** Once a fix is verified and released to the community, we will publicly disclose the vulnerability (typically via a GitHub Security Advisory) and credit you for the discovery.

### What to Include in Your Report

To help us act quickly, please ensure your email includes:

*   **A clear, concise description of the vulnerability.**
*   **Exact steps to reproduce the issue** (including a proof-of-concept script or screenshots, if possible).
*   **The potential impact** (e.g., Remote Code Execution, Information Disclosure, Denial of Service).
*   **Your preferred name or handle** for credit when the advisory goes public (optional).

### Scope of the Policy

This security policy applies to all core components maintained in this repository, specifically:
- `snapfix-backend/` (The Python FastAPI server, LiteLLM integrations, and SQLite DB)
- `snapfix-vscode/` (The TypeScript extension logic, WebView panels, and Terminal hooks)

---

Thank you for helping us keep Snapfix secure! 🔐
