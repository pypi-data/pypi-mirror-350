import sys
from typing import Annotated, Optional

import typer

from alr_spec.utils.empty_template import create_from_empty_template
from alr_spec.utils.from_pkgbuild import (
    PkgbuildDownloader,
    create_from_pkgbuild,
)

app = typer.Typer()


def process_empty_template(output_file: str):
    """Handles creation from an empty template."""
    typer.echo("Creating spec from an empty template...")
    create_from_empty_template(output_file)


def process_from_aur(package_name: str, output_file: str):
    """Handles creation from an AUR package."""
    typer.echo(
        f"Downloading PKGBUILD for package '{package_name}' from AUR..."
    )
    try:
        content = PkgbuildDownloader.download_and_extract(package_name)
        create_from_pkgbuild(content, output_file)
    except Exception as e:
        typer.echo(
            f"Error downloading PKGBUILD for '{package_name}': {e}", err=True
        )
        sys.exit(1)


def process_from_pkgbuild(file_path: str, output_file: str):
    """Handles creation from a local PKGBUILD file."""
    typer.echo(f"Reading PKGBUILD from local file '{file_path}'...")
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        create_from_pkgbuild(content, output_file)
    except IOError as e:
        typer.echo(f"Error reading file '{file_path}': {e}", err=True)
        sys.exit(1)


@app.command(help="Create spec (empty, from PKGBUILD or AUR)")
def create(
    from_aur: Annotated[
        Optional[str], typer.Option(help="Package name to fetch from AUR")
    ] = None,
    from_pkgbuild: Annotated[
        Optional[str], typer.Option(help="Path to local PKGBUILD file")
    ] = None,
    empty_template: Annotated[
        Optional[bool], typer.Option(help="Create spec from an empty template")
    ] = None,
):
    """Main function to handle spec creation."""
    output_file = "alr.sh"

    if empty_template:
        process_empty_template(output_file)
    elif from_aur:
        process_from_aur(from_aur, output_file)
    elif from_pkgbuild:
        process_from_pkgbuild(from_pkgbuild, output_file)
    else:
        typer.echo(
            "No valid option provided. Use --help for usage details.", err=True
        )
        sys.exit(1)
