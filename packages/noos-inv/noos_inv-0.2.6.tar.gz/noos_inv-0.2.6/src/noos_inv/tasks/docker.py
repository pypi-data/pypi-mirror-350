import os

from invoke import Context, task

from noos_inv import exceptions, types, validators


CONFIG = {
    "docker": {
        # Sensitive
        "repo": None,
        "user": "AWS",
        "token": None,
        "arg": None,
        # Non-sensitive
        "name": "webserver",
        "context": ".",
        "file": "Dockerfile",
        "tag": "test",
    }
}


# Docker deployment workflow:


@task()
def login(
    ctx: Context,
    repo: str | None = None,
    user: str | None = None,
    token: str | None = None,
) -> None:
    """Login to Docker remote registry (AWS ECR or Dockerhub)."""
    user = user or ctx.docker.user
    if user == types.UserType.AWS:
        _aws_login(ctx, repo)
    else:
        _dockerhub_login(ctx, user, token)


def _aws_login(ctx: Context, repo: str | None) -> None:
    repo = repo or ctx.docker.repo
    if repo is None:
        raise exceptions.UndefinedVariable("Missing remote AWS ECR URL")
    cmd = "aws ecr get-login-password | "
    cmd += f"docker login --username AWS --password-stdin {repo}"
    ctx.run(cmd)


def _dockerhub_login(ctx: Context, user: str, token: str | None) -> None:
    token = token or ctx.docker.token
    if token is None:
        raise exceptions.UndefinedVariable("Missing remote Dockerhub token")
    ctx.run(f"docker login --username {user} --password {token}")


@task()
def configure(ctx: Context, builder: str = "multi-platform-builder") -> None:
    """Create and provision buildx builder for multi-platform."""
    # Register QEMU with the kernel so that Docker can emulate other architectures.
    ctx.run("docker run --rm --privileged multiarch/qemu-user-static --reset -p yes")
    # Create and use the buildx builder
    ctx.run(f"docker buildx create --name {builder} --use")
    ctx.run("docker buildx inspect --bootstrap")


@task()
def build(
    ctx: Context,
    name: str | None = None,
    context: str | None = None,
    file: str | None = None,
    arg: str | None = None,
) -> None:
    """Build Docker image locally."""
    name = name or ctx.docker.name
    context, file = _get_build_context(ctx, context, file)
    cmd = f"docker build --pull --file {file} --tag {name} "
    cmd += _get_build_arg_fragment(ctx, arg)
    cmd += f"{context}"
    ctx.run(cmd)


@task(help={"keep-source": "Whether to keep the source Docker image (full long name)"})
def pull(
    ctx: Context,
    repo: str | None = None,
    name: str | None = None,
    tag: str = "latest",
    keep_source: bool = False,
) -> None:
    """Pull Docker image from a remote registry."""
    repo = repo or ctx.docker.repo
    name = name or ctx.docker.name
    if repo is None:
        raise exceptions.UndefinedVariable("Missing remote Docker registry URL")
    # ALWAYS pull latest image unless specified
    target_name = f"{repo}/{name}:{tag}"
    ctx.run(f"docker pull {target_name}")
    if not keep_source:
        ctx.run(f"docker tag {target_name} {name}")
        ctx.run(f"docker image rm {target_name}")


@task(
    help={
        "tag-only": "Whether to not tag the Docker image as latest",
        "dry-run": "Whether to only tag the Docker image and to not push",
    }
)
def push(
    ctx: Context,
    repo: str | None = None,
    name: str | None = None,
    tag: str | None = None,
    tag_only: bool = False,
    dry_run: bool = False,
) -> None:
    """Push Docker image to a remote registry."""
    repo = repo or ctx.docker.repo
    name = name or ctx.docker.name
    tag = tag or ctx.docker.tag
    if repo is None:
        raise exceptions.UndefinedVariable("Missing remote Docker registry URL")
    tag_list = [tag] if tag_only else [tag, "latest"]
    for t in tag_list:
        target_name = f"{repo}/{name}:{t}"
        ctx.run(f"docker tag {name} {target_name}")
        if not dry_run:
            ctx.run(f"docker push {target_name}")


@task(help={"tag-only": "Whether to not tag the Docker image as latest"})
def buildx(
    ctx: Context,
    repo: str | None = None,
    name: str | None = None,
    context: str | None = None,
    file: str | None = None,
    arg: str | None = None,
    platform: str = "linux/arm64,linux/amd64",
    tag: str | None = None,
    tag_only: bool = False,
) -> None:
    """Build and push x-platform Docker image to a remote registry."""
    # :Warning:
    # Without using `--push` option to push the image, expect the error:
    # ```No output specified with docker-container driver.
    # Build result will only remain in the build cache.```
    # To push image into registry use `--push`
    # or to load image into docker use `--load`
    # In addition: `--load` option does not work for multiple platforms
    repo = repo or ctx.docker.repo
    name = name or ctx.docker.name
    context, file = _get_build_context(ctx, context, file)
    tag = tag or ctx.docker.tag
    tag_list = [tag] if tag_only else [tag, "latest"]
    for t in tag_list:
        target_name = f"{repo}/{name}:{t}"
        cmd = f"docker buildx build --pull --file {file} --tag {target_name} "
        cmd += _get_build_arg_fragment(ctx, arg)
        cmd += f"--platform {platform} --push "
        cmd += f"{context}"
        ctx.run(cmd)


def _get_build_context(ctx: Context, context: str | None, file: str | None) -> tuple[str, str]:
    context = context or ctx.docker.context
    file = file or f"{context}/{ctx.docker.file}"
    validators.check_path(context)
    validators.check_path(file)
    return (context, file)


def _get_build_arg_fragment(ctx: Context, arg: str | None) -> str:
    arg = arg or ctx.docker.arg
    cmd = ""
    if arg is not None:
        if arg not in os.environ:
            raise exceptions.UndefinedVariable(f"Missing environment variable {arg}")
        cmd += f"--build-arg {arg}={os.environ[arg]} "
    return cmd
