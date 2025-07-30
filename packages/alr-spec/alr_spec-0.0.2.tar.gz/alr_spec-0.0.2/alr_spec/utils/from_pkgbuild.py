import os
import shutil
import sys
import tempfile

import git
import tree_sitter_bash as tsbash
from tree_sitter import Language, Parser

from alr_spec.replacers.arch_replacer import ArchReplacer
from alr_spec.replacers.simple_replacer import SimpleReplacer
from alr_spec.replacers.sources import SourcesReplacer

HEADER = """#
# WARNING: Automatically converted from PKGBUILD and may contain errors
#
"""


class PkgbuildDownloader:
    """Handles downloading PKGBUILD and associated files."""

    @staticmethod
    def download_and_extract(pkgname: str) -> bytes:
        aur_url = f"https://aur.archlinux.org/{pkgname}.git"

        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                print(f"Cloning repository for {pkgname}...")
                git.Repo.clone_from(aur_url, tmpdirname)
                print(f"Files for {pkgname} downloaded to {tmpdirname}")

                PkgbuildDownloader._copy_files(tmpdirname)

                with open(os.path.join(tmpdirname, "PKGBUILD"), "rb") as f:
                    return f.read()

            except Exception as e:
                print(f"Error downloading repository: {e}", file=sys.stderr)
                sys.exit(1)

    @staticmethod
    def _copy_files(tmpdirname: str):
        """Copies all files to the current directory."""
        for root, dirs, files in os.walk(tmpdirname):
            dirs[:] = [d for d in dirs if d not in [".git"]]
            files = [f for f in files if f not in ["PKGBUILD", ".SRCINFO"]]

            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, tmpdirname)
                destination_path = os.path.join(os.getcwd(), relative_path)

                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy(file_path, destination_path)


class ShellReplacerProcessor:
    """Processes PKGBUILD files with replacers."""

    def __init__(self):
        self.parser = self._initialize_parser()

    @staticmethod
    def _initialize_parser() -> Parser:
        bash_language = Language(tsbash.language())
        return Parser(bash_language)

    def process(self, content: bytes, replacers: list) -> bytes:
        tree = self.parser.parse(content)

        for replacer_class in replacers:
            replacer = replacer_class(content, tree)
            content = replacer.process()
            tree = self.parser.parse(content, tree)

        return content


def create_from_pkgbuild(content: bytes, output_file: str):
    """Creates a new spec file from a PKGBUILD."""
    processor = ShellReplacerProcessor()

    replacers = [
        SimpleReplacer,
        ArchReplacer,
        SourcesReplacer,
    ]

    try:
        new_content = processor.process(content, replacers)
        new_content = bytes(HEADER, encoding="utf-8") + new_content

        with open(output_file, "wb") as f:
            f.write(new_content)

        print(f"File successfully written to {output_file}.")
    except IOError as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)
