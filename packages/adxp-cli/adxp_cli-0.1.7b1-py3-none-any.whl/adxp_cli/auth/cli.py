import click
import json
import os
from click import secho
from adxp_sdk.auth.credentials import Credentials
from adxp_cli.auth.service import get_config_file_path, load_config_file
from adxp_cli.auth.schema import AuthConfig


@click.group()
def auth():
    """Command-line interface for AIP Authentication"""
    pass


@auth.command()
@click.option("--username", prompt=True, help="username")
@click.option("--password", prompt=True, hide_input=True, help="password")
@click.option("--client-id", prompt=True, help="client_id")
@click.option(
    "--base-url",
    prompt=True,
    default="https://aip.sktai.io",
    show_default=True,
    help="API base URL",
)
def login(username, password, client_id, base_url):
    """A.X Platform에 로그인하고 정보를 저장합니다."""
    try:
        credentials = Credentials(
            username=username, password=password, client_id=client_id, base_url=base_url
        )
        token = credentials.token
        auth_config = AuthConfig(
            username=username,
            client_id=client_id,
            base_url=base_url,
            token=token,
        ).model_dump()
        adxp_config_path = get_config_file_path(make_dir=True)
        with open(adxp_config_path, "w") as f:
            json.dump(auth_config, f, indent=2)
        secho(
            "Login successful. Authentication information has been saved.", fg="green"
        )
    except Exception as e:
        secho(f"Login failed: {e}", fg="red")


@auth.command()
def refresh():
    """저장된 인증 정보를 사용해 토큰을 갱신하고 config 파일을 업데이트합니다."""
    try:
        adxp_config_path = get_config_file_path(make_dir=False)
        auth_config = load_config_file(adxp_config_path)
        secho("Enter your password to refresh the token.", fg="yellow")
        password = click.prompt("password", hide_input=True)
        credentials = Credentials(
            username=auth_config.username,
            password=password,
            client_id=auth_config.client_id,
            base_url=auth_config.base_url,
        )
        token = credentials.token
        auth_config.token = token
        with open(adxp_config_path, "w") as f:
            json.dump(auth_config.model_dump(), f, indent=2)
        secho("Token has been successfully refreshed.", fg="green")
    except FileNotFoundError:
        secho(
            "🔐 Authentication information file does not exist. Please login first.",
            fg="red",
        )
    except Exception as e:
        secho(f"Failed to refresh token: {e}", fg="red")


@auth.command()
def logout():
    """저장된 인증 정보를 삭제합니다."""
    adxp_config_path = get_config_file_path(make_dir=False)
    if not os.path.exists(adxp_config_path):
        secho("Authentication information file does not exist. Please login first.", fg="red")
        return
    os.remove(adxp_config_path)
    secho("🔐 Authentication information has been successfully deleted.", fg="green")
