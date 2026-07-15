# Architecture

The repository is organized around a simple offline licensing flow:

- Client creates an activation request using a stable HWID.
- License server signs a payload that includes customer, product, edition, expiry, and feature flags.
- Client verifies signature, HWID binding, and expiry before allowing the app to run.

Planned extensions:

- Registry or SQLite-backed storage
- Trial state and usage tracking
- ECDSA support
- Feature-gated APIs and sample plugins
