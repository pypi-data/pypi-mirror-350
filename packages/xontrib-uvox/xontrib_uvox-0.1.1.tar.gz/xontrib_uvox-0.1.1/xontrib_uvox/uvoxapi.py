"""
API for UVox

UVox defines several events related to the life cycle of virtual environments:

* ``uvox_on_create(env: str) -> None``
* ``uvox_on_activate(env: str, path: pathlib.Path) -> None``
* ``uvox_on_deactivate(path: pathlib.Path) -> None``
* ``uvox_on_delete(env: str) -> None``
"""

# TODO: use prompt somehow

import copy
import logging
import os.path
import pathlib
import shutil
import subprocess  # noqa: S404  # We good
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Self, Sequence, cast

from uv import find_uv_bin
from xonsh.events import events
from xonsh.platform import ON_POSIX, ON_WINDOWS

from xontrib_uvox.utils import get_env_safe, get_str_env_var, get_path_var

events.doc(
    "uvox_on_create",
    dedent(
        """\
        uvox_on_create(env: str) -> None

        Fired after an environment is created.
        """,
    ),
)

events.doc(
    "uvox_on_activate",
    dedent(
        """\
        uvox_on_activate(env: str, path: pathlib.Path) -> None

        Fired after an environment is activated.
        """
    ),
)

events.doc(
    "uvox_on_deactivate",
    dedent(
        """\
        uvox_on_deactivate(env: str, path: pathlib.Path) -> None

        Fired after an environment is deactivated.
        """
    ),
)

events.doc(
    "uvox_on_delete",
    dedent(
        """\
        uvox_on_delete(env: str) -> None

        Fired after an environment is deleted (through vox).
        """,
    ),
)


@dataclass
class VirtualEnvironment:
    root: pathlib.Path
    bin: pathlib.Path

    def exists(self) -> bool:
        pyvenv_cfg_path = self.bin.parent / "pyvenv.cfg"
        if not pyvenv_cfg_path.exists():
            return False
        # This would check the actual PEP 405 criterion but it's too slow
        # for line in pyvenv_cfg_path.open():
        #     if line.startswith("home ="):
        #         return True
        return True

    @classmethod
    def make(cls, root_dir: pathlib.Path) -> Self:
        root_dir = root_dir.resolve()

        if ON_WINDOWS:
            bin_dir = root_dir / "Scripts"
        elif ON_POSIX:
            bin_dir = root_dir / "bin"
        else:
            raise OSError("This OS is not supported.")

        return cls(root=root_dir, bin=bin_dir)


class EnvironmentInUseError(Exception):
    """The given environment is currently activated, and the operation cannot be performed."""

    pass


class NoEnvironmentActiveError(Exception):
    """No environment is currently activated, and the operation cannot be performed."""

    pass


class Uvox:
    """API access to Vox and virtual environments.

    Makes use of the VirtualEnvironment namedtuple:

    1. ``root``: The full path to the environment
    2. ``bin``: The full path to the bin directory of the environment
    """

    def __init__(self):
        env = get_env_safe()
        if (venv_home_var := get_str_env_var("VIRTUALENV_HOME", env=env)) is None:
            home_path = pathlib.Path.home()
            self.venvdir = (home_path / ".virtualenvs").resolve()
            # FIXME: is that right?
            env["VIRTUALENV_HOME"] = str(self.venvdir)
        else:
            self.venvdir = pathlib.Path(venv_home_var)
        self.old_env: dict[str, Any] = dict()

    def create(
        self,
        name: str,
        interpreter: str | None = None,
        system_site_packages: bool = False,
        prompt: str | None = None,
    ) -> pathlib.Path:
        """Create a virtual environment in `$VIRTUALENV_HOME` with uv.

        Parameters
        ----------
        name : str
            Virtual environment name
        interpreter: str
            Python interpreter used to create the virtual environment.
            Can be configured via the $UVOX_DEFAULT_INTERPRETER environment variable.
        system_site_packages : bool
            If True, the system (global) site-packages dir is available to
            created environments.
        prompt: str
            Provides an alternative prompt prefix for this environment.
        """
        options = ["--seed"]
        if interpreter is None:
            if (interpreter := get_str_env_var("UVOX_DEFAULT_INTERPRETER")) is not None:
                options.extend(["--python", interpreter])
                logging.info(
                    f"Using default interpreter: {interpreter} (from $UVOX_DEFAULT_INTERPRETER)"
                )
            logging.info("Using uv's default interpreter")
        else:
            options.extend(["--python", interpreter])
            logging.info(f"Using interpreter {interpreter}")
        if prompt is not None:
            options.extend(["--prompt", prompt])
        if system_site_packages:
            options.append("--system-site-packages")

        if "/" in name:
            env_path = pathlib.Path(name)
        else:
            env_path = self.venvdir / name

        cmd = [
            find_uv_bin(),
            "venv",
            *options,
            str(env_path),
        ]

        logging.debug(f"Running {cmd}")

        subprocess.check_call(cmd)  # noqa: S603  # är ok

        events.uvox_on_create.fire(name=name)

        return env_path

    def get_env(self, name_or_path: str | pathlib.Path) -> VirtualEnvironment:
        """Get information about a virtual environment.

        Parameters
        ----------
        name: str Virtual environment name or path.
        """
        res: VirtualEnvironment
        if isinstance(name_or_path, pathlib.Path):
            res = VirtualEnvironment.make(name_or_path)
            if not res.exists():
                raise ValueError(f"Environement {name_or_path} not found.")
            return res
        else:
            # Priority to absolute path if it exists
            if (res := VirtualEnvironment.make(pathlib.Path(name_or_path))).exists():
                return res
            elif (res := VirtualEnvironment.make(self.venvdir / name_or_path)).exists():
                return res
            else:
                raise ValueError(f"Environement {name_or_path} not found.")

    def get_venv_env(self, name_or_path: str | pathlib.Path) -> dict[str, Any]:
        """Return an environment dict correspon"""
        ve = self.get_env(name_or_path)
        return {
            **get_env_safe().detype(),
            "PATH": os.path.pathsep.join([str(ve.bin), *cast(list[str], get_env_safe()["PATH"])]),
            "VIRTUAL_ENV": name_or_path,
        }

    def list_envs(self) -> Sequence[str]:
        """List available virtual environments found in $VIRTUALENV_HOME."""
        return [config_file.parent.name for config_file in self.venvdir.glob("*/pyvenv.cfg")]

    def active(self) -> VirtualEnvironment | None:
        """Get the active virtual environment.

        Returns None if no environment is active.
        """
        if (env_path_or_name := get_str_env_var("VIRTUAL_ENV")) is None:
            return None

        return self.get_env(env_path_or_name)

    def activate(self, name: str):
        """
        Activate a virtual environment.

        Parameters
        ----------
        name : str
            Virtual environment name or absolute path.
        """

        if self.active() is not None:
            self.deactivate()

        env = get_env_safe()
        path_var = get_path_var(env=env)
        self.old_env = {"PATH": copy.copy(path_var.paths)}
        if (python_home := env.pop("PYTHONHOME", None)) is not None:
            self.old_env["PYTHONHOME"] = python_home

        ve = self.get_env(name)
        path_var.prepend(ve.bin)
        env["VIRTUAL_ENV"] = ve.root

        events.uvox_on_activate.fire(name=name, path=ve.root)

    def deactivate(self):
        """
        Deactivate the active virtual environment.
        """
        if (ve := self.active()) is None:
            raise NoEnvironmentActiveError("No environment currently active.")

        env = get_env_safe()
        env.pop("VIRTUAL_ENV")
        env.update(self.old_env)
        self.old_env = dict()

        events.uvox_on_deactivate.fire(path=ve.root)

    def del_env(self, name_or_path: str, silent: bool = False):
        """
        Permanently deletes a virtual environment.

        Parameters
        ----------
        name : str
            Virtual environment name or absolute path.
        """
        env_root = self.get_env(name_or_path).root.resolve()
        if (active := self.active()) is not None and active.root.resolve() == env_root:
            raise EnvironmentInUseError(f'The "{name_or_path}" environment is currently active.')

        # TODO: make these more prompt-toolkit-y
        if not silent:
            print(f"The directory {env_root}")
            print("and all of its content will be deleted.")
            answer = input("Do you want to continue? [Y/n]")
            if "n" in answer.lower():
                return

        shutil.rmtree(env_root)

        events.uvox_on_delete.fire(name=name_or_path)
