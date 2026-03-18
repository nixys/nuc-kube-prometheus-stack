# NUC Kube Prometheus Stack

Helm chart for rendering Prometheus Operator monitoring resources from declarative values.

The chart does not install Prometheus, Alertmanager, or the full `kube-prometheus-stack`. It only renders Prometheus Operator CRD objects that are already supported by the target cluster. The local e2e flow bundles upstream CRDs under `tests/e2e/crds/` only to validate installability.

## Quick Start

Render the example configuration:

```bash
helm template nuc-kube-prometheus-stack . -f values.yaml.example
```

Install the chart:

```bash
helm install nuc-kube-prometheus-stack . \
  --namespace observability \
  --create-namespace \
  -f values.yaml.example
```

Install the local README generator hook:

```bash
pre-commit install
pre-commit install-hooks
```

## Supported Resources

The chart can render these Prometheus Operator kinds:

- `ServiceMonitor`
- `ScrapeConfig`
- `PrometheusRule`
- `Probe`
- `PodMonitor`

Support for individual fields still depends on the Prometheus Operator version and CRDs installed in the cluster.

## Values Model

Each top-level list in [values.yaml](values.yaml) maps to one resource kind:

- `serviceMonitors`
- `scrapeConfigs`
- `prometheusRules`
- `probes`
- `podMonitors`

Every list item uses the same generic contract:

| Field | Required | Description |
|-------|----------|-------------|
| `enabled` | no | Set to `false` to keep a list item in values only for documentation or staged activation. |
| `name` | yes | Resource name. |
| `namespace` | no | Namespace for the resource. Defaults to the Helm release namespace. |
| `labels` | no | Labels merged on top of built-in chart labels and `commonLabels`. |
| `annotations` | no | Annotations merged on top of `commonAnnotations`. |
| `apiVersion` | no | Per-resource API version override. |
| `spec` | no | Raw resource spec rendered as-is. |
| `status` | no | Optional raw status block. Usually not managed through Helm in production. |

Global controls:

- `nameOverride`
- `commonLabels`
- `commonAnnotations`
- `apiVersions.*`

The values contract is validated by [values.schema.json](values.schema.json).

## Helm Values

This section is generated from [values.yaml](values.yaml) by `helm-docs`. Edit [values.yaml](values.yaml) comments or [docs/README.md.gotmpl](docs/README.md.gotmpl), then run `pre-commit run helm-docs --all-files` or `make docs` if you need to refresh it outside a commit.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| apiVersions.podMonitor | string | `"monitoring.coreos.com/v1"` | Default apiVersion for PodMonitor resources. |
| apiVersions.probe | string | `"monitoring.coreos.com/v1"` | Default apiVersion for Probe resources. |
| apiVersions.prometheusRule | string | `"monitoring.coreos.com/v1"` | Default apiVersion for PrometheusRule resources. |
| apiVersions.scrapeConfig | string | `"monitoring.coreos.com/v1alpha1"` | Default apiVersion for ScrapeConfig resources. |
| apiVersions.serviceMonitor | string | `"monitoring.coreos.com/v1"` | Default apiVersion for ServiceMonitor resources. |
| commonAnnotations | object | `{}` | Extra annotations applied to every rendered resource. |
| commonLabels | object | `{}` | Extra labels applied to every rendered resource. |
| nameOverride | string | `""` | Override the default chart label name if needed. |
| podMonitors | list | `[{"annotations":{},"apiVersion":"monitoring.coreos.com/v1","enabled":false,"labels":{},"name":"placeholder-pod-monitor","namespace":"monitoring","spec":{},"status":{}}]` | PodMonitor resources to render. |
| podMonitors[0].annotations | object | `{}` | Resource-specific annotations merged on top of commonAnnotations. |
| podMonitors[0].apiVersion | string | `"monitoring.coreos.com/v1"` | Optional per-resource apiVersion override. |
| podMonitors[0].enabled | bool | `false` | Set to false to keep a list item in values only for documentation or staged activation. |
| podMonitors[0].labels | object | `{}` | Resource-specific labels merged on top of commonLabels and chart labels. |
| podMonitors[0].name | string | `"placeholder-pod-monitor"` | Resource name. |
| podMonitors[0].namespace | string | `"monitoring"` | Namespace for the resource. Defaults to the release namespace when omitted. |
| podMonitors[0].spec | object | `{}` | Raw resource spec rendered as-is. |
| podMonitors[0].status | object | `{}` | Optional raw resource status rendered as-is. |
| probes | list | `[{"annotations":{},"apiVersion":"monitoring.coreos.com/v1","enabled":false,"labels":{},"name":"placeholder-probe","namespace":"monitoring","spec":{},"status":{}}]` | Probe resources to render. |
| probes[0].annotations | object | `{}` | Resource-specific annotations merged on top of commonAnnotations. |
| probes[0].apiVersion | string | `"monitoring.coreos.com/v1"` | Optional per-resource apiVersion override. |
| probes[0].enabled | bool | `false` | Set to false to keep a list item in values only for documentation or staged activation. |
| probes[0].labels | object | `{}` | Resource-specific labels merged on top of commonLabels and chart labels. |
| probes[0].name | string | `"placeholder-probe"` | Resource name. |
| probes[0].namespace | string | `"monitoring"` | Namespace for the resource. Defaults to the release namespace when omitted. |
| probes[0].spec | object | `{}` | Raw resource spec rendered as-is. |
| probes[0].status | object | `{}` | Optional raw resource status rendered as-is. |
| prometheusRules | list | `[{"annotations":{},"apiVersion":"monitoring.coreos.com/v1","enabled":false,"labels":{},"name":"placeholder-prometheus-rule","namespace":"monitoring","spec":{},"status":{}}]` | PrometheusRule resources to render. |
| prometheusRules[0].annotations | object | `{}` | Resource-specific annotations merged on top of commonAnnotations. |
| prometheusRules[0].apiVersion | string | `"monitoring.coreos.com/v1"` | Optional per-resource apiVersion override. |
| prometheusRules[0].enabled | bool | `false` | Set to false to keep a list item in values only for documentation or staged activation. |
| prometheusRules[0].labels | object | `{}` | Resource-specific labels merged on top of commonLabels and chart labels. |
| prometheusRules[0].name | string | `"placeholder-prometheus-rule"` | Resource name. |
| prometheusRules[0].namespace | string | `"monitoring"` | Namespace for the resource. Defaults to the release namespace when omitted. |
| prometheusRules[0].spec | object | `{}` | Raw resource spec rendered as-is. |
| prometheusRules[0].status | object | `{}` | Optional raw resource status rendered as-is. |
| scrapeConfigs | list | `[{"annotations":{},"apiVersion":"monitoring.coreos.com/v1alpha1","enabled":false,"labels":{},"name":"placeholder-scrape-config","namespace":"monitoring","spec":{},"status":{}}]` | ScrapeConfig resources to render. |
| scrapeConfigs[0].annotations | object | `{}` | Resource-specific annotations merged on top of commonAnnotations. |
| scrapeConfigs[0].apiVersion | string | `"monitoring.coreos.com/v1alpha1"` | Optional per-resource apiVersion override. |
| scrapeConfigs[0].enabled | bool | `false` | Set to false to keep a list item in values only for documentation or staged activation. |
| scrapeConfigs[0].labels | object | `{}` | Resource-specific labels merged on top of commonLabels and chart labels. |
| scrapeConfigs[0].name | string | `"placeholder-scrape-config"` | Resource name. |
| scrapeConfigs[0].namespace | string | `"monitoring"` | Namespace for the resource. Defaults to the release namespace when omitted. |
| scrapeConfigs[0].spec | object | `{}` | Raw resource spec rendered as-is. |
| scrapeConfigs[0].status | object | `{}` | Optional raw resource status rendered as-is. |
| serviceMonitors | list | `[{"annotations":{},"apiVersion":"monitoring.coreos.com/v1","enabled":false,"labels":{},"name":"placeholder-service-monitor","namespace":"monitoring","spec":{},"status":{}}]` | ServiceMonitor resources to render. |
| serviceMonitors[0].annotations | object | `{}` | Resource-specific annotations merged on top of commonAnnotations. |
| serviceMonitors[0].apiVersion | string | `"monitoring.coreos.com/v1"` | Optional per-resource apiVersion override. |
| serviceMonitors[0].enabled | bool | `false` | Set to false to keep a list item in values only for documentation or staged activation. |
| serviceMonitors[0].labels | object | `{}` | Resource-specific labels merged on top of commonLabels and chart labels. |
| serviceMonitors[0].name | string | `"placeholder-service-monitor"` | Resource name. |
| serviceMonitors[0].namespace | string | `"monitoring"` | Namespace for the resource. Defaults to the release namespace when omitted. |
| serviceMonitors[0].spec | object | `{}` | Raw resource spec rendered as-is. |
| serviceMonitors[0].status | object | `{}` | Optional raw resource status rendered as-is. |

## Included Values Files

- [values.yaml](values.yaml): documentation-friendly defaults that still render no resources because placeholder items are disabled.
- [values.yaml.example](values.yaml.example): complete example covering every supported resource type.

Use [values.yaml.example](values.yaml.example) as a starting point and remove the sections you do not need.

## Testing

The repository uses three test layers:

- `tests/units/` for `helm-unittest` suites and backward compatibility checks
- `tests/e2e/` for local kind-based Helm install checks against bundled Prometheus Operator CRDs
- `tests/smokes/` for render and schema smoke scenarios

Representative local commands:

```bash
helm lint . -f values.yaml.example
helm template nuc-kube-prometheus-stack . -f values.yaml.example
helm unittest -f 'tests/units/*_test.yaml' .
sh tests/units/backward_compatibility_test.sh
python3 tests/smokes/run/smoke.py --scenario example-render
make test-e2e
```

Detailed test documentation is available in [docs/TESTS.MD](docs/TESTS.MD).

Local setup instructions for the development and test toolchain are available in [docs/DEPENDENCY.md](docs/DEPENDENCY.md).

The `e2e` layer is intentionally kept out of GitLab CI and is expected to be run locally through [Makefile](Makefile) or directly via `tests/e2e/test-e2e.sh`.

## Notes

- Keep the chart API versions aligned with the Prometheus Operator CRDs installed in the cluster.
- `ScrapeConfig` is rendered as `monitoring.coreos.com/v1alpha1` by default in upstream CRDs.
- Prefer managing `spec` through Helm and let controllers own `status`.

## Repository Layout

| Path | Purpose |
|------|---------|
| [Chart.yaml](Chart.yaml) | Chart metadata. |
| [values.yaml](values.yaml) | Minimal default values and `helm-docs` source comments. |
| [docs/README.md.gotmpl](docs/README.md.gotmpl) | Template used by `helm-docs` to build `README.md`. |
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | Local hooks, including automatic `helm-docs` generation on commit. |
| [values.yaml.example](values.yaml.example) | Full example configuration. |
| [values.schema.json](values.schema.json) | JSON schema for chart values. |
| [templates/](templates) | One template per supported Prometheus Operator kind plus shared helpers. |
| [tests/units/](tests/units) | Compact Helm unit suites and backward compatibility checks. |
| [tests/e2e/](tests/e2e) | kind-based end-to-end installation checks with bundled CRDs. |
| [tests/smokes/](tests/smokes) | Smoke scenarios for render and schema validation. |
| [docs/DEPENDENCY.md](docs/DEPENDENCY.md) | Local dependency installation guide for development and tests. |
| [docs/TESTS.MD](docs/TESTS.MD) | Detailed testing documentation. |
