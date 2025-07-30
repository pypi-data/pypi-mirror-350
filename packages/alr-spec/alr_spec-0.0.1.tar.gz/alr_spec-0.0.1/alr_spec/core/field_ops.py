import os

from alr_spec.core.replacer_factory import get_version_replacer_class
from alr_spec.core.utils import run_bash_command
from alr_spec.utils.from_pkgbuild import ShellReplacerProcessor


def _resolve_alr_path(package_path: str) -> str:
    if os.path.isfile(package_path):
        return os.path.abspath(package_path)

    candidate = os.path.join(package_path, "alr.sh")
    if not os.path.isfile(candidate):
        raise FileNotFoundError(
            f"'alr.sh' не найден в директории {package_path}"
        )
    return os.path.abspath(candidate)


def set_field_in_file(field: str, value: str, package_path: str = ".") -> None:
    file_path = _resolve_alr_path(package_path)

    with open(file_path, "rb") as f:
        pr = ShellReplacerProcessor()
        content = f.read()
        new_content = pr.process(
            content, [get_version_replacer_class(field, value)]
        )

    with open(file_path, "wb") as f:
        f.write(new_content)


def get_field_from_file(field: str, package_path: str = ".") -> str:
    file_path = _resolve_alr_path(package_path)
    command = f"source {file_path} && printf '%s\\n' \"${{{field}[@]}}\""
    return run_bash_command(command)
