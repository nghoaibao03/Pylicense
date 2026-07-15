# PyLicense

Offline licensing framework demo for Python applications.

## What it includes

- RSA key generation
- HWID binding on Windows with fallback fingerprinting on other platforms
- Local 30-day trial state on first run
- SQLite-backed trial state under `.pylicense/state.db`
- A reusable `client_sdk` facade for embedding in other Python apps
- Offline activation request / response
- Signed license payloads
- Trial and expiry validation
- Simple CLI utilities for client and server flows

## Layout

```text
Pylicense/
├── activation_tool/
├── admin_cli/
├── key_generator/
├── license_server/
├── sample_app/
├── src/pylicense/
└── docs/
```
