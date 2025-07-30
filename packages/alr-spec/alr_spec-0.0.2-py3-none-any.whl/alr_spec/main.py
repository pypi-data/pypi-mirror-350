import typer

from alr_spec.commands.build import app as build_app
from alr_spec.commands.checksums import app as checksums_app
from alr_spec.commands.create import app as create_app
from alr_spec.commands.field import app as field_app
from alr_spec.commands.update import app as update_package_app

app = typer.Typer()

app.add_typer(create_app)
app.add_typer(build_app)
app.add_typer(checksums_app)
app.add_typer(field_app)
app.add_typer(update_package_app)


def main():
    app()


if __name__ == "__main__":
    main()
