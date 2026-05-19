import subprocess


def run(command, cwd=None):

    print(f"\n➡️ Running: {' '.join(command)}\n")

    subprocess.run(
        command,
        cwd=cwd,
        check=True
    )