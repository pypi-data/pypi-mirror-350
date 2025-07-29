import json
import logging
import pathlib

from invoke import Context, task

from noos_inv import exceptions, types, validators


logger = logging.getLogger(__name__)


CONFIG = {
    "local": {
        # Sensitive
        "config": None
    }
}


# Local development workflow

@task(help={
    "command": "Parameter to provide the template e.g. django-cadmin or isodate",
    "param_name": "Name of the template parameter e.g. command or isodate",
    "namespace": "Argo namespace to use",
    "template": "Template name to use e.g. gateway-worker-template"
})
def argo_submit(
    ctx: Context,
    command: str = "",
    namespace: str = "noos-core",
    template: str = "gateway-worker-template",
    param_name: str = "command",
):
    if command is None:
        raise exceptions.UndefinedVariable("Missing command")
    template_path = f"wftmpl/{template}"
    template_cmd = f"{param_name}={command}"
    base_cmd = "ARGO_SECURE=false argo -s localhost:2746 submit"
    cmd = f'{base_cmd} -n {namespace} --from {template_path} -p "{template_cmd}"'
    try:
        ctx.run(cmd)
    except Exception as e:
        logger.error("Make sure that the port forward to the argo server is running.")
        logger.error("Install argo CLI via https://argo-workflows.readthedocs.io/en/latest/walk-through/argo-cli/")
        raise e

@task(help={"force": "Whether to destroy the existing file first"})
def dotenv(
    ctx: Context,
    template: str = "./dotenv.tpl",
    target: str = "./.env",
    force: bool = False,
) -> None:
    """Create local dotenv file."""
    validators.check_path(template)
    try:
        validators.check_path(target)
        if force:
            raise exceptions.PathNotFound
    except exceptions.PathNotFound:
        ctx.run(f"cp {template} {target}")


@task(
    help={
        "pod": "Forward port only for this specific pod",
        "unforward": "Unforward ports without forwarding them again",
        "config": "Configuration file path (including pods to port-forward)",
    }
)
def ports(
    ctx: Context,
    pod: str | None = None,
    unforward: bool = False,
    config: str | None = None,
) -> None:
    """Forward ports for defined Kubernetes pods."""
    config = config or ctx.local.config
    if config is None:
        raise exceptions.UndefinedVariable("Missing local config file")
    # Load config file
    validators.check_path(config)
    with pathlib.Path(config).open(mode="rt") as f:
        local_config: types.PodsConfig = json.load(f).get("podForwards")
    validators.check_config(local_config)
    # Narrow-down config if necessary
    tmp_config: types.PodsConfig
    if pod is None:
        tmp_config = local_config
    else:
        if pod not in local_config:
            raise exceptions.UndefinedVariable("Missing pod in config file")
        tmp_config = {pod: local_config[pod]}
    # Iterate over targeted services
    filtered_pods = _filter_pods(ctx, tmp_config)
    for pod, pod_config in tmp_config.items():
        if unforward:
            # Unforward port
            _unforward(ctx, pod_config)
        else:
            # Forward port
            _forward(ctx, pod_config, filtered_pods[pod])


def _filter_pods(ctx: Context, config: types.PodsConfig) -> dict[str, str]:
    """Filter all matching pods in a given namespace."""
    # Query all pods in the namespace
    cmd_tpl = "kubectl get pod -n {namespace} "
    # Select only the name
    cmd_tpl += "-o=custom-columns=NAME:.metadata.name "
    # Filter out pods with the prefix
    cmd_tpl += " | grep {prefix}"
    # Build data struct {service: pod_name}
    selected_pods: dict[str, str] = {}
    for pod, pod_config in config.items():
        cmd = cmd_tpl.format(
            namespace=pod_config["podNamespace"],
            prefix=pod_config["podPrefix"],
        )
        result = ctx.run(cmd, hide=True)
        if result is None:
            logger.error(f"Failed to fetch pod name for {pod}. Skip!")
            continue
        selected_pods[pod] = result.stdout.rstrip()
    # Return selected pod names for each service
    return selected_pods


def _get_kubectl_command(
    *, namespace: str, name: str, port: int, local_port: int, local_address: str | None = None
) -> str:
    """Get the command to forward a port to a pod."""
    cmd = f"kubectl port-forward -n {namespace} {name} {local_port}:{port}"
    if local_address is not None:
        cmd += f" --address={local_address}"
    return cmd


def _forward(ctx: Context, config: types.PodConfig, pod_name: str) -> None:
    """Forward port matching configuration."""
    # Build kubectl port-forward command
    cmd = _get_kubectl_command(
        namespace=config["podNamespace"],
        name=pod_name,
        port=config["podPort"],
        local_port=config["localPort"],
        local_address=config.get("localAddress"),
    )
    # Ensure the process is detached
    cmd += " </dev/null >/dev/null 2>&1 &"
    logger.warning(f"Forwarding {config['podNamespace']}/{pod_name} to :{config['localPort']}")
    ctx.run(cmd, warn=True, hide=True)


def _unforward(ctx: Context, config: types.PodConfig) -> None:
    """Unforward port matching configuration."""
    # Build kubectl port-forward command
    cmd = _get_kubectl_command(
        namespace=config["podNamespace"],
        name=config["podPrefix"] + ".*",
        port=config["podPort"],
        local_port=config["localPort"],
    )
    # Fetch running processes
    cmd = f"ps aux | grep '{cmd}' | grep -v grep"
    # Restrict to only pid part
    cmd += " | awk '{print $2}'"
    result = ctx.run(cmd, warn=True, hide=True)
    # Kill the process
    if result is not None:
        if result.stdout != "":
            logger.warning(f"Killing port-forward at :{config['localPort']}")
            ctx.run(f"kill -9 {result.stdout.rstrip()}", warn=True, hide=True)
