import os
import subprocess

import typer

app = typer.Typer()

IMAGE = "ghcr.io/aides-infra/buildbot-worker-builder-sisyphus-x86_64:0.0.7"
BUILD_COMMAND = (
    "cd /app && /bin/aides-update-cache && /bin/alr fix &&"
    + "/bin/alr -i=false build -s $(pwd)/alr.sh"
)


@app.command(help="Build package from spec in isolated environment")
def build(
    no_cache: bool = typer.Option(False, "--no-cache", help="Disable cache")
):
    command = f"source {os.getcwd()}/alr.sh && echo $name"

    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result)
        exit(-1)

    package_name = result.stdout.strip()

    cache_dir = os.path.join(
        os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
        "alr-spec",
        "builds",
        package_name,
    )

    try:
        command = [
            "docker",
            "run",
            "-it",
            "--rm",
            "--device",
            "/dev/fuse",
            "--cap-add=SYS_ADMIN",
            "-v",
            f"{os.getcwd()}:/app",
        ]

        if not no_cache:
            alr_cache = os.path.join(cache_dir, "alr")
            os.makedirs(alr_cache, exist_ok=True)
            command.extend(["-v", f"{alr_cache}:/var/cache/alr"])

            apt_archives = os.path.join(cache_dir, "apt_archives")
            os.makedirs(apt_archives, exist_ok=True)
            os.makedirs(os.path.join(apt_archives, "partial"), exist_ok=True)
            command.extend(["-v", f"{apt_archives}:/var/cache/apt/archives"])

        command.extend([IMAGE, "/bin/sh", "-c", BUILD_COMMAND])

        print(" ".join(command))

        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error while running docker: {e}")
    except FileNotFoundError:
        typer.echo("Docker is not installed or not in PATH.")
