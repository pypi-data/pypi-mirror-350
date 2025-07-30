import hashlib
import os
from pathlib import Path
from typing import List
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

from alr_spec.core.field_ops import get_field_from_file
from alr_spec.core.utils import run_bash_command
from alr_spec.replacers.base import BaseReplacer
from alr_spec.replacers.sources import Utils
from alr_spec.utils.from_pkgbuild import ShellReplacerProcessor


def _download_file(url: str, dest_folder: Path) -> Path:
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    local_folder = dest_folder / url_hash
    local_folder.mkdir(parents=True, exist_ok=True)

    local_filename = local_folder / "file"
    if not local_filename.exists():
        print(f"Downloading file from {url}...")
        try:
            response = requests.get(url, stream=True, timeout=10000)
            response.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Saved to {local_filename}")
        except requests.RequestException as e:
            raise RuntimeError(f"Download error: {e}")
    return local_filename


def _calculate_hash(file_path: Path, algorithm="sha256") -> str:
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def _get_replacer_class(checksums_field: str, values: List[str]):
    class ChecksumsReplacer(BaseReplacer):
        def process(self):
            def find_replacements(node):
                for child in node.children:
                    if child.type == "variable_assignment":
                        var_node, value_node = Utils.parse_variable_assignment(
                            child
                        )
                        if self._node_text(var_node) == checksums_field:
                            lst = "\n  ".join(values)
                            self.replaces.append(
                                {
                                    "node": value_node,
                                    "content": f"(\n  {lst}\n)",
                                }
                            )

            find_replacements(self.tree.root_node)
            return self._apply_replacements()

    return ChecksumsReplacer


def remove_query_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    for param in ["~name"]:
        query_params.pop(param, None)

    new_query = urlencode(query_params, doseq=True)

    new_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment,
        )
    )

    return new_url


def _update_checksums_for_field(
    script_path: Path, field: str, cache_dir: Path
):
    print(f"Updating checksums for {field}")

    sources = get_field_from_file("sources", script_path).splitlines()
    checksums_field = field.replace("sources", "checksums")

    checksums = []
    for url in sources:
        url = remove_query_params(url)
        file_path = _download_file(url, cache_dir)
        hash_value = _calculate_hash(file_path)
        checksums.append(f"sha256:{hash_value}")

    with open(script_path, "rb") as f:
        pr = ShellReplacerProcessor()
        content = f.read()
        new_content = pr.process(
            content, [_get_replacer_class(checksums_field, checksums)]
        )

    with open(script_path, "wb") as f:
        f.write(new_content)


def update_all_checksums(package_path: str = ".", sources_field: str = ""):
    abs_path = Path(package_path).resolve()
    script_path = abs_path if abs_path.is_file() else abs_path / "alr.sh"

    if not script_path.exists():
        raise FileNotFoundError(f"{script_path} not found")

    command = f"source {script_path} && compgen -v | grep '^sources'"
    if sources_field:
        fields = [sources_field]
    else:
        fields = run_bash_command(command).splitlines()

    cache_dir = (
        Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
        / "alr-spec"
        / "downloads"
    )

    for field in fields:
        _update_checksums_for_field(script_path, field, cache_dir)
