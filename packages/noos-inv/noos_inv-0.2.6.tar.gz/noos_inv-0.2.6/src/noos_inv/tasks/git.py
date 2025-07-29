from invoke import Context, task

from noos_inv import exceptions


CONFIG = {
    "git": {
        "token": None,
    }
}


@task()
def config(ctx: Context, token: str | None = None) -> None:
    """Setup git credentials with a Github token."""
    token = token or ctx.git.token
    if token is None:
        raise exceptions.UndefinedVariable("Missing Github token")
    ctx.run("git config --global --unset url.ssh://git@github.com.insteadof")
    ctx.run(f"echo https://{token}:@github.com > ~/.git-credentials")
    ctx.run("git config --global credential.helper store")
