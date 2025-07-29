# Using `invoke` as a library
# http://docs.pyinvoke.org/en/stable/concepts/library.html


from invoke import Collection, Config, Program

from noos_inv import __version__
from noos_inv.tasks import docker, git, helm, local, python, terraform


class BaseConfig(Config):
    prefix = "noosinv"


namespace = Collection()
namespace.add_collection(Collection.from_module(docker, config=docker.CONFIG))
namespace.add_collection(Collection.from_module(git, config=git.CONFIG))
namespace.add_collection(Collection.from_module(helm, config=helm.CONFIG))
namespace.add_collection(Collection.from_module(local, config=local.CONFIG))
namespace.add_collection(Collection.from_module(python, config=python.CONFIG))
namespace.add_collection(Collection.from_module(terraform, config=terraform.CONFIG))


program = Program(namespace=namespace, config_class=BaseConfig, version=__version__)
