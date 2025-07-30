import typer

from alr_spec.core.field_ops import get_field_from_file, set_field_in_file

app = typer.Typer()


@app.command(help="Set field in alr.sh")
def set_field(
    field: str,
    value: str,
    package_path: str = typer.Option(
        ".", help="Путь к alr.sh или к папке, где он находится"
    ),
):
    set_field_in_file(field, value, package_path)


@app.command(help="Get field from alr.sh")
def get_field(
    field: str,
    package_path: str = typer.Option(
        ".", help="Путь к alr.sh или к папке, где он находится"
    ),
):
    result = get_field_from_file(field, package_path)
    print(result)
