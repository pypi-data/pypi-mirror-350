"""
Salt execution module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "relenv"


def __virtual__():
    return __virtualname__


def fetch(arch: str = None, python: str = None, user: str = None):
    """
    Fetch the tools to build a relenv environment.

    CLI Example:

    .. code-block:: bash

        salt '*' relenv.fetch arch=amd64 python=3.10.17
    """
    exe = __grains__["pythonexecutable"]
    args = [exe, "-m", "relenv", "fetch"]
    if arch:
        args.append(f"--arch={arch}")
    if python:
        args.append(f"--python={python}")
    return __salt__["cmd.run"](args, python_shell=False, runas=user)


def toolchain(arch=None, clean: bool = False, crosstool_only: bool = False, user: str = None):
    """
    Fetch the toolchain to build c extensions for a relenv environment.

    CLI Example:

    .. code-block:: bash

        salt '*' relenv.toolchain arch=amd64 clean=True crosstool_only=True
    """
    exe = __grains__["pythonexecutable"]
    args = [exe, "-m", "relenv", "toolchain", "fetch"]
    if arch:
        args.append(f"--arch={arch}")
    if clean:
        args.append("--clean")
    if crosstool_only:
        args.append("--crosstool-only")
    return __salt__["cmd.run"](args, python_shell=False, runas=user)


def create(
    name: str,
    venv_bin=None,
    arch=None,
    python=None,
    clean: bool = False,
    crosstool_only: bool = False,
    user: str = None,
    **kwargs,
):
    """
    Create a relenv environment in the named directory.

    CLI Example:

    .. code-block:: bash

        salt '*' relenv.create /opt/my_relenv arch=amd64 python=3.10.17
    """
    exe = __grains__["pythonexecutable"]
    if venv_bin:
        args = [venv_bin, "create", name]
    else:
        args = [exe, "-m", "relenv", "create", name]
    if arch:
        args.append(f"--arch={arch}")
    if python:
        args.append(f"--python={python}")

    # Ensure that the proper build tools exist
    ret = fetch(arch, python, user=user)
    if not ret["retcode"] == 0:
        return ret
    ret = toolchain(arch, clean=clean, crosstool_only=crosstool_only, user=user)
    if not ret["retcode"] == 0:
        return ret

    return __salt__["cmd.run"](args, python_shell=False, runas=user)
