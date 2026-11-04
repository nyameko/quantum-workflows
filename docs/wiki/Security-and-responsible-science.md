# Security, quotas and responsible scientific results

Local simulations are generally credential-free; QPU services, GPU nodes and provider sessions can consume finite shared budgets or money. Seek explicit approval and record account/project attribution before launching a costly experiment. Do not run load tests against provider backends without consent.

Keep provider tokens, cloud keys, patient/personnel data, protected datasets, kubeconfig and research SSH private keys out of notebooks, sample result manifests, public PRs and agent memory. Use approved secret brokers and scrub operational logs. The platform performs authorisation; this repository's source cannot grant an allocation.

Report unsupported accuracy/precision claims clearly. Simulation results, noisy hardware measurements and experimentally validated scientific effects are separate evidentiary classes. For nuclear/medical/security use cases, an educational algorithm is not clinical or safety certification.

See [SECURITY.md](https://github.com/nyameko/quantum-workflows/blob/main/SECURITY.md) and [runner credentials](https://github.com/nyameko/quantum-workflows/blob/main/docs/ARCHITECTURE.md).