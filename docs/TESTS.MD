# Tests

This repository uses three local test layers:

- `tests/units/` for `helm-unittest` suites and backward compatibility rendering checks
- `tests/smokes/` for render-path and schema validation without a live cluster
- `tests/e2e/` for local kind-based installation against real Prometheus Operator CRDs

The layers are complementary:

- unit tests check chart-owned behavior
- smoke tests check end-to-end rendering and validation tooling
- e2e checks that the rendered manifests can actually be installed in Kubernetes

## Running Unit Tests

Run all Helm unit suites:

```bash
helm unittest -f 'tests/units/*_test.yaml' .
```

Run the backward-compatibility script:

```bash
sh tests/units/backward_compatibility_test.sh
```

Notes:

- value file paths inside the unit suites are resolved relative to `tests/units/`
- the backward-compatibility script requires git tags to be available locally
- because the chart is generic, unit tests focus on namespacing, labels, annotations, and `apiVersion` behavior rather than deep CRD payload semantics

## Unit Coverage

The current unit suites cover:

1. default empty renders
2. helper-driven metadata merges
3. release-namespace fallback
4. per-resource and per-kind `apiVersion` overrides
5. representative manifests from `values.yaml.example`

## Smoke Tests

Smoke tests live under `tests/smokes/`.

The structure is intentionally split into small reusable layers:

- `run/` contains the entry point
- `scenarios/` orchestrates complete smoke flows
- `steps/` contains reusable operations
- `fixtures/` contains dedicated smoke-test values files

## Directory Layout

```text
tests/smokes/
├── helpers/
│   └── argparser.py
├── fixtures/
│   ├── invalid-list-contract.values.yaml
│   ├── invalid-missing-name.values.yaml
│   ├── null-override.values.yaml
│   └── rendering-contract.values.yaml
├── run/
│   └── smoke.py
├── scenarios/
│   └── smoke.py
├── steps/
│   ├── chart.py
│   ├── helm.py
│   ├── kubeconform.py
│   ├── render.py
│   └── system.py
└── requirements.txt
```

## Covered Smoke Scenarios

1. `default-empty`
   Verifies that the chart renders no manifests with default values.

2. `schema-invalid-list-contract`
   Verifies that `values.schema.json` rejects the legacy list-based values contract now that resource collections are maps.

3. `schema-invalid-missing-name`
   Verifies that `values.schema.json` is active and rejects a resource item without `name`.

4. `rendering-contract`
   Verifies chart-owned behavior rather than CRD payload content:
   - `nameOverride`
   - merged labels and annotations
   - namespace fallback for namespaced resources
   - global and per-resource `apiVersion` override behavior

5. `null-override`
   Verifies that a resource map entry can be explicitly nulled out by an overlay values file without breaking render output for the remaining resources.

6. `example-render`
   Renders `values.yaml.example` and verifies that all supported resource kinds are produced from the example configuration.

7. `example-kubeconform`
   Renders `values.yaml.example` and validates the result with `kubeconform` using the same Prometheus Operator CRD schema location as CI.

## Smoke Prerequisites

- `python3`
- `helm`
- `kubeconform` for the `example-kubeconform` scenario
- `PyYAML`

Install Python dependency:

```bash
pip3 install -r tests/smokes/requirements.txt
```

## Running Smoke Tests

Run all smoke tests:

```bash
python3 tests/smokes/run/smoke.py
```

Equivalent `Makefile` targets:

```bash
make test-smoke
make test-smoke-fast
```

Run a subset:

```bash
python3 tests/smokes/run/smoke.py --scenario rendering-contract
python3 tests/smokes/run/smoke.py --scenario example-render
```

## E2E Tests

End-to-end tests live under `tests/e2e/`.

This layer uses a shell runner around `kind` and Helm to validate that the chart can be installed into a real API server with Prometheus Operator CRDs present.

## E2E Layout

```text
tests/e2e/
├── crds/
│   ├── crd-podmonitors.yaml
│   ├── crd-probes.yaml
│   ├── crd-prometheusrules.yaml
│   ├── crd-scrapeconfigs.yaml
│   └── crd-servicemonitors.yaml
├── kind.yaml
├── test-e2e.sh
└── values/
    └── install.values.yaml
```

## What the E2E Runner Does

`tests/e2e/test-e2e.sh` performs the following steps:

1. Starts a disposable kind cluster from `tests/e2e/kind.yaml`.
2. Installs bundled Prometheus Operator CRDs from `tests/e2e/crds/`.
3. Runs `helm upgrade --install` against the chart root with `tests/e2e/values/install.values.yaml`.
4. Verifies the installed `ServiceMonitor`, `ScrapeConfig`, `PrometheusRule`, `Probe`, and `PodMonitor` objects with `kubectl get`.
5. Cleans up the kind cluster on exit.

## Running E2E Tests

Run the default end-to-end flow:

```bash
bash tests/e2e/test-e2e.sh
```

Pass additional arguments through to `helm upgrade --install`:

```bash
bash tests/e2e/test-e2e.sh --debug
```

The repository also includes a local convenience [Makefile](../Makefile) for these flows:

```bash
make test-e2e
make test-e2e-debug
make test-e2e-help
```

To pass extra arguments to the shell runner through `make`, use `E2E_ARGS`:

```bash
make test-e2e E2E_ARGS="--debug"
```

## E2E Prerequisites

- `kubectl`
- `helm`
- `docker`
- `kind`

The repository already vendors the CRD manifests needed for e2e, so the runner does not have to download them at runtime. Docker may still need network access if the requested `kindest/node` image is not cached locally.

Optional environment overrides:

- `CLUSTER_NAME`
- `K8S_VERSION`
- `PROMETHEUS_OPERATOR_CRD_DIR`

## Recommended Local Verification

Use this sequence when changing chart logic:

```bash
helm lint . -f values.yaml.example
helm template smoke . -f values.yaml.example >/dev/null
helm unittest -f 'tests/units/*_test.yaml' .
python3 tests/smokes/run/smoke.py --scenario default-empty --scenario schema-invalid-list-contract --scenario schema-invalid-missing-name --scenario rendering-contract --scenario null-override --scenario example-render
sh tests/units/backward_compatibility_test.sh
bash tests/e2e/test-e2e.sh
```

Run the heavier validation steps only when the local toolchain is available:

```bash
python3 tests/smokes/run/smoke.py
make test-e2e
```
