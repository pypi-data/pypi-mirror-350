from invoke import Context, task

from noos_inv import exceptions, types, validators


CONFIG = {
    "python": {
        "install": "uv",
        "source": "./src",
        "formatters": "ruff",
        "linters": "ruff,mypy",
        "tests": "./src/tests",
        "user": None,
        "token": None,
        "numprocesses": 8,
    }
}


# Python deployment workflow


@task()
def clean(ctx: Context) -> None:
    """Clean project from temp files / dirs."""
    ctx.run("rm -rf build dist")
    ctx.run("find src -type d -name __pycache__ | xargs rm -rf")


@task()
def format(
    ctx: Context,
    formatters: str | None = None,
    source: str | None = None,
    install: str | None = None,
) -> None:
    """Auto-format source code."""
    formatters = formatters or ctx.python.formatters
    source = source or ctx.python.source
    validators.check_path(source)
    cmd = _activate_shell(ctx, install)
    for formatter in formatters.split(","):
        match types.FormatterType.get(formatter):
            case types.FormatterType.BLACK:
                ctx.run(cmd + f"black {source}", pty=True)
            case types.FormatterType.ISORT:
                ctx.run(cmd + f"isort {source}", pty=True)
            case types.FormatterType.RUFF:
                ctx.run(cmd + f"ruff check --select I --fix {source}")
                ctx.run(cmd + f"ruff format {source}")


@task()
def lint(
    ctx: Context,
    linters: str | None = None,
    source: str | None = None,
    install: str | None = None,
) -> None:
    """Run python linters."""
    linters = linters or ctx.python.linters
    source = source or ctx.python.source
    validators.check_path(source)
    cmd = _activate_shell(ctx, install)
    for linter in linters.split(","):
        match types.LinterType.get(linter):
            case types.LinterType.BLACK:
                ctx.run(cmd + f"black --check {source}", pty=True)
            case types.LinterType.ISORT:
                ctx.run(cmd + f"isort --check-only {source}", pty=True)
            case types.LinterType.PYDOCSTYLE:
                ctx.run(cmd + f"pydocstyle {source}", pty=True)
            case types.LinterType.FLAKE8:
                ctx.run(cmd + f"flake8 {source}", pty=True)
            case types.LinterType.MYPY:
                ctx.run(cmd + f"mypy {source}", pty=True)
            case types.LinterType.RUFF:
                ctx.run(cmd + f"ruff check {source}")
            case types.LinterType.IMPORTS:
                ctx.run(cmd + "lint-imports", pty=True)


@task()
def test(
        ctx: Context,
        tests: str | None = None,
        group: str = "",
        install: str | None = None,
        numprocesses: int = 0,
) -> None:
    """Run pytest with optional grouped tests."""
    tests = tests or ctx.python.tests
    numprocesses = numprocesses or ctx.python.numprocesses
    if group != "":
        tests += "/" + types.GroupType.get(group)
    validators.check_path(tests)
    cmd = _activate_shell(ctx, install)
    pytest_cmd = "pytest"
    if numprocesses > 1:
        pytest_cmd += f" --numprocesses={numprocesses}"
    pytest_cmd += f" {tests}"
    ctx.run(cmd + pytest_cmd, pty=True)


@task()
def coverage(
    ctx: Context,
    config: str = "setup.cfg",
    report: str = "term",
    tests: str | None = None,
    install: str | None = None,
) -> None:
    """Run coverage test report."""
    tests = tests or ctx.python.tests
    validators.check_path(tests)
    cmd = _activate_shell(ctx, install)
    ctx.run(cmd + f"pytest --cov --cov-config={config} --cov-report={report} {tests}", pty=True)


@task()
def package(ctx: Context, install: str | None = None) -> None:
    """Build project wheel distribution."""
    install = install or ctx.python.install
    match types.InstallType.get(install):
        case types.InstallType.POETRY:
            ctx.run("poetry build", pty=True)
        case types.InstallType.PIPENV:
            ctx.run("pipenv run python -m build -n", pty=True)
        case types.InstallType.UV:
            ctx.run("uvx --from build pyproject-build --installer uv")


@task()
def release(
    ctx: Context, user: str | None = None, token: str | None = None, install: str | None = None
) -> None:
    """Publish wheel distribution to PyPi."""
    user = user or ctx.python.user
    token = token or ctx.python.token
    install = install or ctx.python.install
    if user is None:
        raise exceptions.UndefinedVariable("Missing remote PyPi registry user")
    if token is None:
        raise exceptions.UndefinedVariable("Missing remote PyPi registry token")
    match types.InstallType.get(install):
        case types.InstallType.POETRY:
            ctx.run(f"poetry publish --build -u {user} -p {token}", pty=True)
        case types.InstallType.PIPENV:
            ctx.run(f"pipenv run twine upload dist/* -u {user} -p {token}", pty=True)
        case types.InstallType.UV:
            ctx.run(f"uvx twine upload dist/* -u {user} -p {token}")


def _activate_shell(ctx: Context, install: str | None) -> str:
    install = install or ctx.python.install
    return f"{types.InstallType.get(install)} run "
