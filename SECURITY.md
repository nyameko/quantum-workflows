# Security policy

Report credential exposure privately and revoke the affected credential immediately.

Provider API keys are bearer secrets. They must not appear in source code, notebooks, images,
Slurm scripts, logs, result manifests, or committed configuration. Local direct execution uses a
Qiskit saved account or ephemeral environment variables. On the facility, QRMI/SPANK or the future
`quantum-platform` credential broker injects credentials into the job environment just in time.

SSH and WireGuard public keys stored by `quantum-platform` are identity data but are not equivalent
to provider secrets. Private SSH keys, WireGuard private keys, and provider tokens never belong in
the platform database in plaintext.
