from invoke import Context, task

from noos_inv import exceptions, types, validators


CONFIG = {
    "helm": {
        # Sensitive
        "repo": "local-repo",
        "url": None,
        "user": "AWS",
        "token": None,
        # Non-sensitive
        "plugins": ["https://github.com/chartmuseum/helm-push.git"],
        "chart": "./helm/chart",
        "values": "./local/helm-values.yaml",
        "name": "webserver",
        "tag": "0.1.0",
    }
}


# Helm deployment workflow:


@task()
def login(
    ctx: Context,
    repo: str | None = None,
    url: str | None = None,
    user: str | None = None,
    token: str | None = None,
) -> None:
    """Login to Helm remote registry (AWS ECR or Chart Museum)."""
    repo = repo or ctx.helm.repo
    user = user or ctx.helm.user
    if user == types.UserType.AWS:
        _aws_login(ctx, repo)
    else:
        _cm_login(ctx, user, repo, url, token)


def _aws_login(ctx: Context, repo: str) -> None:
    cmd = "aws ecr get-login-password | "
    cmd += f"helm registry login --username AWS --password-stdin {repo}"
    ctx.run(cmd)


def _cm_login(
    ctx: Context,
    user: str,
    repo: str,
    url: str | None,
    token: str | None,
) -> None:
    url = url or ctx.helm.url
    token = token or ctx.helm.token
    if url is None:
        raise exceptions.UndefinedVariable("Missing remote Helm registry url")
    if token is None:
        raise exceptions.UndefinedVariable("Missing remote Helm registry token")
    ctx.run(f"helm repo add {repo} {url} --username {user} --password {token}")


@task(iterable=["plugins"])
def install(ctx: Context, plugins: list[str] | None = None) -> None:
    """Provision local Helm client (Chart Museum Plugin)."""
    plugins = plugins or ctx.helm.plugins
    for plugin in plugins:
        ctx.run(f"helm plugin install {plugin}")


@task()
def lint(ctx: Context, chart=None) -> None:
    """Check compliance of Helm charts / values."""
    chart = chart or ctx.helm.chart
    validators.check_path(chart)
    ctx.run(f"helm lint {chart}")


@task(help={"dry-run": "Whether to render the Helm manifest first"})
def test(
    ctx: Context,
    chart: str | None = None,
    values: str | None = None,
    release: str = "test",
    namespace: str = "default",
    context: str = "minikube",
    dry_run: bool = False,
) -> None:
    """Test local deployment in Minikube."""
    chart = chart or ctx.helm.chart
    values = values or ctx.helm.values
    validators.check_path(chart)
    validators.check_path(values)
    cmd = f"helm install {release} {chart} --values {values} "
    cmd += f"--create-namespace --namespace {namespace} --kube-context {context}"
    if dry_run:
        cmd += " --dry-run --debug"
    ctx.run(cmd)


@task(help={"dry-run": "Whether to package the Helm chart only"})
def push(
    ctx: Context,
    chart: str | None = None,
    repo: str | None = None,
    name: str | None = None,
    tag: str | None = None,
    dry_run: bool = False,
) -> None:
    """Push Helm chart to a remote registry (AWS ECR or Chart Museum)."""
    repo = repo or ctx.helm.repo
    chart = chart or ctx.helm.chart
    validators.check_path(chart)
    if ctx.helm.user == types.UserType.AWS:
        _aws_push(ctx, chart, repo, name, tag, dry_run)
    else:
        _cm_push(ctx, chart, repo, dry_run)


def _aws_push(
    ctx: Context,
    chart: str,
    repo: str,
    name: str | None,
    tag: str | None,
    dry_run: bool,
) -> None:
    names = (name or ctx.helm.name).split("/")
    tag = tag or ctx.helm.tag
    ctx.run(f"helm dependency update {chart}")
    ctx.run(f"helm package {chart} --version {tag}")
    if not dry_run:
        ctx.run(f"helm push {names[-1]}-{tag}.tgz oci://{repo}/{'/'.join(names[:-1])}")


def _cm_push(ctx: Context, chart: str, repo: str, dry_run: bool) -> None:
    ctx.run(f"helm dependency update {chart}")
    if not dry_run:
        ctx.run(f"helm cm-push {chart} {repo}")
