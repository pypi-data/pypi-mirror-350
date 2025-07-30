import typer

from alr_spec.core.checksums import update_all_checksums

app = typer.Typer()


@app.command(help="Update checksums from sources")
def update_checksums(
    package_path: str = typer.Argument(".", help="Путь к alr.sh или папке"),
    sources_field: str = typer.Option(
        "",
        help="Конкретное имя переменной источника (например, sources_extra)",
    ),
):
    try:
        update_all_checksums(package_path, sources_field)
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(code=1)
