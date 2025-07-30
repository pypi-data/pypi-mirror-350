import subprocess
from shlex import split

from hatchling.plugin import hookimpl
from hatchling.version.source.plugin.interface import VersionSourceInterface


class CommandVersionSource(VersionSourceInterface):
    PLUGIN_NAME = "command"

    def get_version_data(self) -> dict[str, str]:
        cmd = self.config["command"]
        version = subprocess.check_output(split(cmd), cwd=self.root).decode().strip()
        return {"version": version}

    def set_version(self, version: str, version_data: dict) -> None:
        pass


@hookimpl
def hatch_register_version_source() -> type[VersionSourceInterface]:
    return CommandVersionSource
