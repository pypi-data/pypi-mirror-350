import sys
import click
import json
import yaml
from typing import TypedDict
import os
from pydantic import BaseModel, Field


def get_python_version() -> str:
    if sys.version_info < (3, 10) or sys.version_info > (3, 13):
        py_version_msg = (
            "\n\nNote: The in-mem server requires Python 3.10 ~ 3.12."
            f" You are currently using Python {sys.version_info.major}.{sys.version_info.minor}."
            ' Please upgrade your Python version before installing "adxp-cli".'
        )
        raise click.UsageError(py_version_msg)

    return ".".join(map(str, sys.version_info[:2]))


# TODO: 개선필요 - file_path를 환경변수 받아서 처리
def save_docker_credentials(username, password):
    """Docker 로그인 정보를 .docker_auth.json에 저장합니다."""
    credentials = {"username": username, "password": password}
    with open(".docker_auth.json", "w") as f:
        json.dump(credentials, f)


def load_docker_credentials():
    """저장된 Docker 로그인 정보를 로드합니다."""
    if not os.path.exists(".docker_auth.json"):
        raise FileNotFoundError("Docker credentials not found. Please login first.")

    with open(".docker_auth.json", "r") as f:
        credentials = json.load(f)
    return credentials.get("username"), credentials.get("password")
