"""
Salt state module
"""
import logging

import salt.states.pip_state as pip
import salt.states.virtualenv_mod as virtualenv

log = logging.getLogger(__name__)

__virtualname__ = "relenv"


def __virtual__():
    return __virtualname__


# Wrappers around pip state


def installed(name: str, relenv: str, **kwargs):
    """
    Make sure that a package is installed in a relenv environment.
    """
    return pip.installed(name, bin_env=relenv, **kwargs)


def removed(name: str, relenv: str, **kwargs):
    """
    Make sure that a package is removed from a relenv environment.
    """
    return pip.removed(name, bin_env=relenv, **kwargs)


def uptodate(name: str, **kwargs):
    """
    Make sure that the relenv environment is up to date.
    """
    return pip.uptodate(bin_env=name, **kwargs)


# Unique relenv states
def managed(
    name,
    arch=None,
    python=None,
    **kwargs,
):
    """
    Manage a relenv environment.
    This state is a wrapper around the virtualenv state, which is
    modified to use the relenv.create function instead of the
    virtualenv.create function.
    """
    old_venv = __salt__.get("virtualenv.create", None)
    __salt__["virtualenv.create"] = __salt__["relenv.create"]
    try:
        return virtualenv.managed(name=name, arch=arch, python=python, **kwargs)
    finally:
        if old_venv:
            __salt__["virtualenv.create"] = old_venv
        else:
            __salt__.pop("virtualenv.create")


def absent(name: str):
    """
    Remove a relenv environment.

    CLI Example:

    .. code-block:: bash

        salt '*' state.single relenv.absent /opt/relenv/myenv
    """
    return __salt__["file.remove"](name, python_shell=False)
