from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from tests.smokes.steps import chart, helm, kubeconform, render, system


@dataclass
class SmokeContext:
    repo_root: Path
    workdir: Path
    chart_dir: Path
    render_dir: Path
    release_name: str
    namespace: str
    kube_version: str
    kubeconform_bin: str
    schema_location: str
    skip_kinds: str

    @property
    def example_values(self) -> Path:
        return self.repo_root / "values.yaml.example"

    @property
    def rendering_contract_values(self) -> Path:
        return self.repo_root / "tests" / "smokes" / "fixtures" / "rendering-contract.values.yaml"

    @property
    def invalid_missing_name_values(self) -> Path:
        return self.repo_root / "tests" / "smokes" / "fixtures" / "invalid-missing-name.values.yaml"

    @property
    def invalid_list_contract_values(self) -> Path:
        return self.repo_root / "tests" / "smokes" / "fixtures" / "invalid-list-contract.values.yaml"

    @property
    def null_override_values(self) -> Path:
        return self.repo_root / "tests" / "smokes" / "fixtures" / "null-override.values.yaml"


def check_default_empty(context: SmokeContext) -> None:
    helm.lint(context.chart_dir, workdir=context.workdir)
    output_path = context.render_dir / "default-empty.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        output_path=output_path,
        workdir=context.workdir,
    )
    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 0)


def check_schema_invalid_missing_name(context: SmokeContext) -> None:
    result = helm.lint(
        context.chart_dir,
        values_file=context.invalid_missing_name_values,
        workdir=context.workdir,
        check=False,
    )
    if result.returncode == 0:
        raise system.TestFailure(
            "helm lint unexpectedly succeeded for invalid values without resource name"
        )

    combined_output = f"{result.stdout}\n{result.stderr}"
    if "name" not in combined_output:
        raise system.TestFailure(
            "helm lint failed for invalid values, but the error does not mention the missing name field"
        )


def check_schema_invalid_list_contract(context: SmokeContext) -> None:
    result = helm.lint(
        context.chart_dir,
        values_file=context.invalid_list_contract_values,
        workdir=context.workdir,
        check=False,
    )
    if result.returncode == 0:
        raise system.TestFailure(
            "helm lint unexpectedly succeeded for legacy list-based values contract"
        )

    combined_output = f"{result.stdout}\n{result.stderr}"
    if "serviceMonitors" not in combined_output or "got array, want object" not in combined_output:
        raise system.TestFailure(
            "helm lint failed for legacy list-based values, but the error does not mention the array-to-object contract mismatch"
        )


def check_rendering_contract(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.rendering_contract_values,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "rendering-contract.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.rendering_contract_values,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 2)

    service_monitor = render.select_document(
        documents, kind="ServiceMonitor", name="merged-service-monitor"
    )
    render.assert_path(service_monitor, "apiVersion", "example.net/v1alpha1")
    render.assert_path(service_monitor, "metadata.namespace", context.namespace)
    render.assert_path(
        service_monitor,
        "metadata.labels[app.kubernetes.io/name]",
        "monitoring-platform",
    )
    render.assert_path(service_monitor, "metadata.labels.stack", "observability")
    render.assert_path(service_monitor, "metadata.labels.component", "service-monitor")
    render.assert_path(service_monitor, "metadata.labels.tier", "edge")
    render.assert_path(service_monitor, "metadata.annotations.team", "platform")
    render.assert_path(service_monitor, "metadata.annotations.note", "external")
    render.assert_path(
        service_monitor,
        "spec.selector.matchLabels[app.kubernetes.io/name]",
        "api",
    )

    prometheus_rule = render.select_document(
        documents, kind="PrometheusRule", name="platform-rules"
    )
    render.assert_path(prometheus_rule, "apiVersion", "example.net/v1beta1")
    render.assert_path(prometheus_rule, "metadata.namespace", "ops-rules")
    render.assert_path(
        prometheus_rule,
        "metadata.labels[app.kubernetes.io/name]",
        "monitoring-platform",
    )
    render.assert_path(prometheus_rule, "metadata.labels.component", "rule")
    render.assert_path(prometheus_rule, "metadata.annotations.team", "platform")
    render.assert_path(prometheus_rule, "metadata.annotations.note", "alerts")
    render.assert_path(prometheus_rule, "spec.groups[0].rules[0].record", "up:sum")


def check_null_override(context: SmokeContext) -> None:
    values_files = [context.example_values, context.null_override_values]
    helm.lint(
        context.chart_dir,
        values_files=values_files,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "null-override.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_files=values_files,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 4)
    render.assert_kinds(
        documents,
        {
            "ScrapeConfig",
            "PrometheusRule",
            "Probe",
            "PodMonitor",
        },
    )
    render.select_document(documents, kind="PodMonitor", name="worker-pod-monitor")


def check_example_render(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.example_values,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "example-render.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 5)
    render.assert_kinds(
        documents,
        {
            "ServiceMonitor",
            "ScrapeConfig",
            "PrometheusRule",
            "Probe",
            "PodMonitor",
        },
    )

    service_monitor = render.select_document(
        documents, kind="ServiceMonitor", name="api-service-monitor"
    )
    render.assert_path(service_monitor, "metadata.namespace", "app-a")
    render.assert_path(service_monitor, "spec.endpoints[0].port", "http-metrics")

    scrape_config = render.select_document(
        documents, kind="ScrapeConfig", name="external-scrape-config"
    )
    render.assert_path(scrape_config, "spec.scheme", "HTTP")
    render.assert_path(
        scrape_config, "spec.staticConfigs[0].targets[1]", "ledger.example.com:8443"
    )

    prometheus_rule = render.select_document(
        documents, kind="PrometheusRule", name="platform-rules"
    )
    render.assert_path(
        prometheus_rule, "spec.groups[0].rules[0].alert", "ApiErrorBudgetBurn"
    )

    probe = render.select_document(documents, kind="Probe", name="blackbox-http")
    render.assert_path(
        probe,
        "spec.targets.staticConfig.static[1]",
        "https://api.example.com/readyz",
    )

    pod_monitor = render.select_document(
        documents, kind="PodMonitor", name="worker-pod-monitor"
    )
    render.assert_path(pod_monitor, "spec.podMetricsEndpoints[0].port", "metrics")


def check_example_kubeconform(context: SmokeContext) -> None:
    output_path = context.render_dir / "example-kubeconform.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        output_path=output_path,
        workdir=context.workdir,
    )
    kubeconform.validate(
        manifest_path=output_path,
        kube_version=context.kube_version,
        kubeconform_bin=context.kubeconform_bin,
        schema_location=context.schema_location,
        skip_kinds=context.skip_kinds,
    )


SCENARIOS: list[tuple[str, Callable[[SmokeContext], None]]] = [
    ("default-empty", check_default_empty),
    ("schema-invalid-list-contract", check_schema_invalid_list_contract),
    ("schema-invalid-missing-name", check_schema_invalid_missing_name),
    ("rendering-contract", check_rendering_contract),
    ("null-override", check_null_override),
    ("example-render", check_example_render),
    ("example-kubeconform", check_example_kubeconform),
]


def run_smoke_suite(args) -> int:
    scenario_map = dict(SCENARIOS)
    requested = args.scenario or ["all"]
    if "all" in requested:
        selected = [name for name, _ in SCENARIOS]
    else:
        selected = requested

    repo_root = Path(args.chart_dir).resolve()
    workdir, chart_dir = chart.stage_chart(repo_root, args.workdir)
    context = SmokeContext(
        repo_root=repo_root,
        workdir=workdir,
        chart_dir=chart_dir,
        render_dir=workdir / "rendered",
        release_name=args.release_name,
        namespace=args.namespace,
        kube_version=args.kube_version,
        kubeconform_bin=args.kubeconform_bin,
        schema_location=args.schema_location,
        skip_kinds=args.skip_kinds,
    )
    context.render_dir.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[str, str]] = []
    try:
        for name in selected:
            system.log(f"=== scenario: {name} ===")
            try:
                scenario_map[name](context)
            except Exception as exc:
                failures.append((name, str(exc)))
                system.log(f"FAILED: {name}: {exc}")
            else:
                system.log(f"PASSED: {name}")
    finally:
        if args.keep_workdir:
            system.log(f"workdir kept at {workdir}")
        else:
            chart.cleanup(workdir)

    if failures:
        system.log("=== summary: failures ===")
        for name, message in failures:
            system.log(f"- {name}: {message}")
        return 1

    system.log("=== summary: all smoke scenarios passed ===")
    return 0
