import os
import subprocess
from abc import ABC
from pathlib import Path
from typing import Tuple

import requests

from alr_spec.core.checksums import update_all_checksums
from alr_spec.core.field_ops import get_field_from_file, set_field_in_file


class BaseUpdater(ABC):
    def update_check(self, package_path: Path) -> Tuple[str, str]: ...

    def update_run(self, package_path: Path, new_version: str) -> None: ...


class CommonUpdater(BaseUpdater):
    def update_check(self, package_path: Path):
        current_version = get_field_from_file("version", str(package_path))
        cmd = "nvchecker -c .nvchecker.toml --logger json | jq -r .version"
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        new_version = result.stdout.strip()
        return current_version, new_version

    def update_run(self, package_path: Path, new_version: str):
        set_field_in_file("version", new_version, str(package_path))
        set_field_in_file("release", "1", str(package_path))
        update_all_checksums(str(package_path), "")
        subprocess.run(["/bin/shfmt", "-l", "-w", "alr.sh"], check=True)


class SnapUpdater(CommonUpdater):
    def update_run(self, package_path: Path, new_version: str):
        snap_name = get_field_from_file("_snap_name", str(package_path))
        snap_channel = get_field_from_file("_snap_channel", str(package_path))

        headers = {"Snap-Device-Series": "16"}
        response = requests.get(
            f"https://api.snapcraft.io/v2/snaps/info/{snap_name}",
            headers=headers,
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()

        channel_map = data.get("channel-map", [])
        for entry in channel_map:
            channel = entry.get("channel", {})
            if channel.get("name") == snap_channel:
                new_version = entry.get("version")
                url = entry.get("download", {}).get("url")
                break
        else:
            raise ValueError(
                f"Channel {snap_channel} not found for snap {snap_name}"
            )

        set_field_in_file("_snap_url", url, str(package_path))
        set_field_in_file("version", new_version, str(package_path))
        set_field_in_file("release", "1", str(package_path))

        update_all_checksums(str(package_path), "")
        subprocess.run(["/bin/shfmt", "-l", "-w", "alr.sh"], check=True)


class Updater(BaseUpdater):
    def __init__(self, fallbackUpdater: BaseUpdater):
        self.updater = fallbackUpdater

    def update_check(self, package_path: Path):
        update_check_script = package_path / ".alr" / "update-check"
        if update_check_script.exists():
            print("Running .alr/update-check...")
            result = subprocess.run(
                [str(update_check_script)],
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            res = result.stdout.split()
            return res[0], res[1]
        else:
            return self.updater.update_check(package_path)

    def update_run(self, package_path: Path, new_version: str):
        update_run_script = package_path / ".alr" / "update-run"
        if update_run_script.exists():
            print("Running .alr/update-run...")
            subprocess.run([str(update_run_script), new_version], check=True)
        else:
            return self.updater.update_run(package_path, new_version)


def update_package_logic(path_to_package: str, no_checksums: bool):
    package_path = Path(path_to_package).resolve()

    if not package_path.exists():
        raise FileNotFoundError(f"Path '{path_to_package}' does not exist.")

    os.chdir(package_path)

    preset = get_field_from_file("_alr_update_preset", package_path)

    if preset == "snap":
        fallbacUpdater = SnapUpdater()
    else:
        fallbacUpdater = CommonUpdater()

    updater = Updater(fallbacUpdater)
    current_version, new_version = updater.update_check(package_path)
    if current_version == new_version:
        print("Nothing to do")
        return
    updater.update_run(package_path, new_version)
