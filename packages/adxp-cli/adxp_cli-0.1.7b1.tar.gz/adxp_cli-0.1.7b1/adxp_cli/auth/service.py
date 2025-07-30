import os
import json
from adxp_cli.auth.schema import AuthConfig
from adxp_sdk.auth.credentials import Credentials
import click


def get_config_file_path(make_dir: bool = False):
    ADXP_CONFIG_PATH = os.getenv("ADXP_CONFIG_PATH")
    if ADXP_CONFIG_PATH is None:
        ADXP_CONFIG_PATH = os.path.expanduser("~/.adxp/config.json")
    if make_dir:
        os.makedirs(os.path.dirname(ADXP_CONFIG_PATH), exist_ok=True)
    elif not os.path.exists(ADXP_CONFIG_PATH):
        raise FileNotFoundError("ADXP_CONFIG_PATH does not exist.")
    return ADXP_CONFIG_PATH


def load_config_file(config_file_path: str) -> AuthConfig:
    with open(config_file_path, "r") as f:
        config = json.load(f)

    return AuthConfig(**config)


def get_credential() -> tuple[dict, AuthConfig]:
    try:
        adxp_config_path = get_config_file_path(make_dir=False)
        config = load_config_file(adxp_config_path)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        headers["Authorization"] = f"Bearer {config.token}"
        return headers, config
    except FileNotFoundError:
        raise click.ClickException(
            "🔐 Authentication information file does not exist. Please login first"
        )
    except Exception as e:
        raise click.ClickException(f"❌ Failed to get credential: {e}")
