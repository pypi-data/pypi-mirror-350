import subprocess
import click

import json
import click
import subprocess


def docker_login(username, password):
    """Docker Hub에 로그인합니다."""
    try:
        cmd = ["docker", "login", "-u", username, "-p", password]
        subprocess.run(cmd, check=True)
        click.secho("Docker login successful", fg="green")
    except subprocess.CalledProcessError:
        click.secho("Docker login failed. Please check your credentials.", fg="red")
        raise click.UsageError("Docker login failed.")
