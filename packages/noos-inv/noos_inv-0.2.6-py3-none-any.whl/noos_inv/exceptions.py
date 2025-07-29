class ValidationError(Exception):
    """Error raised in validating Invoke context variables."""

    pass


class UndefinedVariable(ValidationError):
    """Error raised if a context variable remains undefined."""

    pass


class PathNotFound(ValidationError):
    """Error raised if a filesytem path isn't valid."""

    pass


class InvalidConfig(ValidationError):
    """Error raised in validating a config file schema."""

    pass
