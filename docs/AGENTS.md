# Agent Guide

This file is the reference baseline for Helm chart repositories that follow a single-chart layout with layered tests under `tests/units`, `tests/e2e`, and `tests/smokes`.

Adapt names, chart-specific commands, and controller details to the target project, but keep the structure, discipline, and decision rules consistent unless the repository clearly uses another pattern.

## Repository Shape

Prefer a single root chart with this baseline structure:

```text
.
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── values.yaml.example
├── templates/
├── tests/
│   ├── units/
│   ├── e2e/
│   └── smokes/
└── docs/
```

Keep documentation and automation aligned with the actual tree. If a directory or workflow is removed, update both the docs and CI in the same change.

## Repository Standard

Treat this repository as a template for similar chart repositories:

- one chart at the repository root
- one clear values contract
- one example values file that exercises the full supported surface
- one helper layer for shared template behavior
- one documented test pyramid with fast checks in CI and heavier checks local-first

Do not introduce parallel structures that solve the same problem twice. Avoid duplicate examples, duplicate test fixtures with overlapping intent, or multiple competing local entry points.

## Documentation Rules

- Keep one root `README.md` as the primary entry point.
- Keep `README.md` generated from `docs/README.md.gotmpl` via `helm-docs` and `pre-commit`.
- Keep test-layer details in `docs/TESTS.MD`.
- Keep repository-wide contribution and maintenance guidance in `docs/AGENTS.md`.
- Use relative repository links in Markdown, not workstation-specific absolute paths.
- Prefer describing the current repository state over aspirational tooling that is not actually wired in.
- If a workflow is local-only, state that explicitly.
- When changing versions, commands, or supported resources, update docs in the same change as code and CI.
- When changing chart values, update the `# --` comments in `values.yaml` so the generated Helm values table stays useful.

## Chart Design Expectations

- Keep templates thin and deterministic.
- Centralize shared rendering logic in `templates/_helpers.tpl` when repetition appears.
- Prefer generic resource contracts when the chart is intended to pass through raw CRD specs.
- Validate the values contract with `values.schema.json` when possible.
- Avoid managing `status` in production workflows unless the chart is explicitly intended for fixtures or synthetic manifests.
- Keep defaults minimal and safe. The base `values.yaml` should render nothing unless the repository has a strong reason to ship opinionated resources.
- Keep `values.yaml.example` comprehensive enough to exercise every supported kind at least once.

## Versioning Rules

- Pin Kubernetes-dependent tooling deliberately.
- Treat Kubernetes API validation version, local cluster image version, and CRD bundle version as separate concerns.
- Do not assume the latest Kubernetes patch has a matching `kindest/node` image.
- Do not assume every Prometheus Operator kind is served at the same stability level.
- `ScrapeConfig` may remain `v1alpha1` even when other monitoring resources are `v1`.
- When bumping versions, verify real upstream availability before editing the repository.

## Prometheus Operator Rules

For chart repositories that render Prometheus Operator resources, keep these assumptions explicit:

- chart rendering support and cluster installability are different concerns
- CRD support depends on the operator version installed in the cluster
- `ServiceMonitor`, `PodMonitor`, `Probe`, and `PrometheusRule` can coexist with `ScrapeConfig` even when API maturity differs
- per-kind `apiVersion` overrides are part of the public contract, not a workaround

When testing against pinned CRDs:

- verify which API version is served for each kind
- keep examples and e2e fixtures aligned with the installed CRDs
- explain intentional mismatches between chart defaults and test fixtures

## Test Layers

### Unit Tests

Use `helm-unittest` for chart-owned rendering behavior:

- helper behavior
- defaulting
- label and annotation merges
- namespace handling
- API version overrides
- representative manifests from example values

Keep unit suites compact. Do not mirror large CRD payloads field by field unless the chart itself transforms them.

### Smoke Tests

Use smoke tests for render-path validation without a live cluster:

- default empty render
- schema enforcement from `values.schema.json`
- representative example rendering
- optional `kubeconform` validation

Prefer small reusable helpers around `helm`, file staging, and manifest assertions.

### E2E Tests

Use `kind`-based or cluster-backed e2e tests only when they validate something that unit and smoke tests cannot:

- installation into a real API server
- CRD presence and compatibility
- end-to-end Helm install or upgrade flows

If e2e requires Docker or kind, it is acceptable to keep it local-only and expose it through a `Makefile`.

Prefer direct `helm upgrade --install` in e2e runners unless another orchestration layer provides a concrete benefit that is proven in this repository.

## CI Guidance

CI should cover the lightweight checks by default:

- lint
- unit tests
- smoke tests
- backward compatibility rendering
- manifest rendering
- schema validation

Add e2e to CI only when the target runner environment actually supports it. Avoid documenting e2e CI jobs that cannot run on the repository's real runners.

## Change Discipline

When making repository-wide changes, prefer this order:

1. fix or simplify the implementation
2. align tests and fixtures
3. align CI defaults
4. align documentation
5. run a compact verification pass

Do not leave the repository in a state where the code is correct but docs still describe removed tooling, or CI still points at stale commands.
