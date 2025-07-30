import subprocess


def run_bash_command(command):
    result = subprocess.run(
        ["/bin/bash", "-c", command],
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ошибка при выполнении команды: {result.stderr}")
    return result.stdout.strip()
