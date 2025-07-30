import click
import json
from click import secho
import pathlib
import shutil
from typing import Sequence, Optional
from adxp_cli.agent.docker import (
    generate_graph_dockerfile,
    dockerfile_build,
    create_dockerfile_and_build,
)
from adxp_cli.common.exec import Runner, subp_exec
from adxp_cli.common.progress import Progress
from adxp_cli.agent.validation import (
    validate_graph_yaml,
    LanggraphConfig,
)
from adxp_cli.common.utils import (
    get_python_version,
    save_docker_credentials,
    load_docker_credentials,
)
from adxp_cli.agent.port import docker_login
from adxp_cli.agent.run import run_server
from adxp_cli.auth.service import get_credential
from tabulate import tabulate


@click.group()
def agent():
    """Command-line interface for AIP server management."""
    pass


# 2. Run API Server on Local
@agent.command(help="🖥 Run the API server on local")
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", default=28080, type=int, help="Port number")
@click.option("--graph_yaml", default="./graph.yaml", help="Path to graph.yaml")
def run(host, port, graph_yaml):
    run_server(host, port, graph_yaml)


@agent.command(help="🐳 Generate a Dockerfile for Agent API Server")
@click.option("--output", default="./sktaip.Dockerfile", help="Path to Dockerfile")
@click.option("--graph_yaml", default="./graph.yaml", help="Path to graph.yaml")
def dockerfile(output: str, graph_yaml: str) -> None:
    """Dockerfile 내용을 생성합니다."""
    save_path = pathlib.Path(output).absolute()
    secho(f"🔍 Validating configuration at path: {graph_yaml}", fg="yellow")
    config: LanggraphConfig = validate_graph_yaml(graph_yaml)
    secho("✅ Configuration validated!", fg="green")
    secho(f"📝 Generating Dockerfile at {save_path}", fg="yellow")
    python_version = get_python_version()
    dockerfile_content = generate_graph_dockerfile(config, python_version)
    with open(str(save_path), "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    secho("✅ Created: Dockerfile", fg="green")


@agent.command(help="🐳 Build a Docker image for Agent API Server")
@click.option(
    "--tag",
    "-t",
    help="""Tag for the docker image.

    \b
    Example:
        langgraph build -t my-image

    \b
    """,
    required=True,
)
@click.option(
    "--dockerfile",
    "-f",
    help="""File path to the Dockerfile. If not provided, a Dockerfile will be generated automatically.
    """,
    required=False,
    default=None,
)
@click.option(
    "--base-image",
    hidden=True,
)
@click.option("--graph_yaml", default="./graph.yaml", help="Path to graph.yaml")
@click.option("--pull", is_flag=True, help="Pull the latest base image")
@click.option("--directory", "-d", help="Directory to build the image", default=".")
@click.argument("docker_build_args", nargs=-1, type=click.UNPROCESSED)
def build(
    graph_yaml: str,
    docker_build_args: Sequence[str],
    base_image: Optional[str],
    tag: str,
    pull: bool,
    directory: str,
    dockerfile: Optional[str],
):
    # Docker 설치 확인
    if shutil.which("docker") is None:
        raise click.ClickException("Docker가 설치되어 있지 않습니다.")

    secho(f"🔍 Validating configuration at path: {graph_yaml}", fg="yellow")
    config: LanggraphConfig = validate_graph_yaml(graph_yaml)
    secho("✅ Configuration validated!", fg="green")
    if dockerfile:
        secho(f"📝 Using Dockerfile at {dockerfile}", fg="yellow")
        dockerfile_build(directory, dockerfile, tag, docker_build_args)
    else:
        create_dockerfile_and_build(
            base_image, tag, config, docker_build_args, pull, directory
        )


# TODO: 개선필요 - username, password, client_id 받아서 token을 file로 저장해놓고 플랫폼 API 호출하는 cli에서 사용
# 담당자 - 강선구M


@agent.command(help="Get List of Deployed Agents")
@click.option("--page", default=1, help="page number, default: 1")
@click.option("--size", default=10, help="size of page, default: 10")
@click.option("--search", default=None, help="search app by name")
@click.option(
    "--all", "-a", is_flag=True, default=False, help="show agents with all columns"
)
def ls(page: int, size: int, search: Optional[str], all: bool):
    """Get List of Agents"""
    import requests

    headers, config = get_credential()
    url = f"{config.base_url}/api/v1/agent/agents/apps"

    params = {"page": str(page), "size": str(size), "target_type": "external_graph"}
    if search:
        params["search"] = search

    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 401:
        raise click.ClickException(
            "🔐 401 Unauthorized : Please login again. \n Run Either One of the Following Commands \n 1. adxp-cli auth login \n 2. adxp-cli auth refresh"
        )
    if res.status_code == 200:
        data = res.json().get("data")
        if data:
            # 테이블로 정제해서 출력
            table = []
            if all:
                headers_ = [
                    "id",
                    "name",
                    "description",
                    "created_at",
                    "updated_at",
                    "versions",
                ]
                for item in data:
                    versions = ", ".join(
                        str(d.get("version"))
                        for d in item.get("deployments", [])
                        if d.get("version") is not None
                    )
                    row = [
                        item.get("id", ""),
                        item.get("name", ""),
                        item.get("description", ""),
                        item.get("created_at", ""),
                        item.get("updated_at", ""),
                        versions,
                    ]
                    table.append(row)
            else:
                headers_ = ["id", "name", "versions"]
                for item in data:
                    versions = ", ".join(
                        str(d.get("version"))
                        for d in item.get("deployments", [])
                        if d.get("version") is not None
                    )
                    row = [
                        item.get("id", ""),
                        item.get("name", ""),
                        versions,
                    ]
                    table.append(row)
            click.secho("✅ Deployed Custom Agent APPs:", fg="green")
            click.echo(
                tabulate(table, headers=headers_, tablefmt="github", showindex=True)
            )
        else:
            click.secho("⚠️ No deployed custom agent apps found.", fg="yellow")
    else:
        raise click.ClickException(
            f"❌ Failed to get deployed custom agent apps: {res.status_code}\n{res.text}"
        )


# @cli.command(help="🚀 Deploy agent to AIP server")
# # @click.option("--username", prompt=True, help="Login username")
# # @click.option("--password", prompt=True, hide_input=True, help="Login password")
# # @click.option("--client-id", prompt=True, help="OAuth client ID")
# @click.option("--token", default=None, help="Access token (if already known)")
# # def deploy_agent(username, password, client_id, token):
# def deploy_agent(token):
#     """에이전트를 AIP 서버에 배포합니다."""

#     # def get_token(username, password, client_id):
#     def get_token():
#         login_url = "https://aip.sktai.io/api/v1/auth/login"
#         login_data = {
#             "grant_type": "",
#             "username": "admin",
#             "password": "aisnb",
#             "scope": "",
#             "client_id": "default",
#             "client_secret": "",
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded",
#             "accept": "application/json",
#         }
#         res = requests.post(login_url, data=login_data, headers=headers)
#         if res.status_code == 201:
#             return res.json().get("access_token")
#         raise click.ClickException(f"🔐 로그인 실패: {res.status_code}, {res.text}")

#     if not token:
#         # token = get_token(username, password, client_id)
#         token = get_token()

#     url = "https://aip.sktai.io/api/v1/agent/agents/apps/workforce-app"
#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

# files = {
#     "env_file": (None, ".env"),  # 빈 파일
#     "name": (None, "interpretation agent"),
#     "description": (None, "Workforce tax agent: interpretation"),
#     "target_type": (None, "external_graph"),
#     "model_list": (None, "GIP/gpt-4o"),
#     "image_tag": (None, "tax-interpretation-v0.2.1")
# }

# secho(f"🚀 Deploying agent to {url}", fg="cyan")
# res = requests.post(url, headers=headers, files=files)
# .env 파일 경로 읽기
# env_file_path = os.path.join(os.path.dirname(__file__), ".env")
# if not os.path.isfile(env_file_path):
#     raise click.ClickException(f".env 파일을 찾을 수 없습니다: {env_file_path}")

# with open(env_file_path, "rb") as f:
#     files = {
#         "env_file": ("env_file", f),
#         "name": (None, "interpretation agent"),
#         "description": (None, "Workforce tax agent: interpretation"),
#         "target_type": (None, "external_graph"),
#         "model_list": (None, "GIP/gpt-4o"),
#         "image_tag": (None, "tax-interpretation-v0.2.1"),
#     }

#     secho(f"🚀 Deploying agent to {url}", fg="cyan")
#     res = requests.post(url, headers=headers, files=files)
# if res.status_code in (200, 201):
#     secho("✅ Agent successfully deployed!", fg="green")
# else:
#     raise click.ClickException(f"❌ 배포 실패: {res.status_code}\n{res.text}")

# app_id = res.json().get("data", {}).get("app_id")
# deployment_id = res.json().get("data", {}).get("deployment_id")
# if app_id:
#     click.secho(f"✅ 배포 성공! App ID: {app_id}", fg="green")
# else:
#     raise click.ClickException("⚠️ 'app_id'를 응답에서 찾을 수 없습니다.")

# if deployment_id:
#     click.secho(f"✅ 배포 성공! Deployment ID: {deployment_id}", fg="green")
# else:
#     raise click.ClickException("⚠️ 'deployment_id'를 응답에서 찾을 수 없습니다.")


# @cli.command(help="🔍 Get deployment by deployment_id")
# @click.option("--deployment-id", required=True, help="Deployment ID to fetch")
# @click.option("--token", default=None, help="Access token (optional)")
# def get_deployment(deployment_id, token):
#     def get_token():
#         login_url = "https://aip.sktai.io/api/v1/auth/login"
#         login_data = {
#             "grant_type": "",
#             "username": "admin",
#             "password": "",
#             "scope": "",
#             "client_id": "default",
#             "client_secret": "",
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded",
#             "accept": "application/json",
#         }
#         res = requests.post(login_url, data=login_data, headers=headers)
#         if res.status_code == 201:
#             return res.json().get("access_token")
#         raise click.ClickException(f"🔐 로그인 실패: {res.status_code}\n{res.text}")

#     if not token:
#         token = get_token()

#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

#     url = f"https://aip.sktai.io/api/v1/agent/agents/apps/deployments/{deployment_id}"
#     click.secho(f"🔍 Getting deployment for ID: {deployment_id}", fg="cyan")

#     res = requests.get(url, headers=headers)
#     if res.status_code == 200:
#         data = res.json().get("data")
#         if data:
#             click.secho("✅ Deployment 정보:", fg="green")
#             click.echo(json.dumps(data, indent=2, ensure_ascii=False))
#         else:
#             click.secho("⚠️ Deployment 데이터를 찾을 수 없습니다.", fg="yellow")
#     else:
#         raise click.ClickException(
#             f"❌ Deployment 조회 실패: {res.status_code}\n{res.text}"
#         )


# @cli.command(help="🗑️ Delete deployment by deployment_id")
# @click.option("--deployment-id", required=True, help="Deployment ID to delete")
# @click.option("--token", default=None, help="Access token (optional)")
# def delete_deployment(deployment_id, token):
#     def get_token():
#         login_url = "https://aip.sktai.io/api/v1/auth/login"
#         login_data = {
#             "grant_type": "",
#             "username": "admin",
#             "password": "aisnb",
#             "scope": "",
#             "client_id": "default",
#             "client_secret": "",
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded",
#             "accept": "application/json",
#         }
#         res = requests.post(login_url, data=login_data, headers=headers)
#         if res.status_code == 201:
#             return res.json().get("access_token")
#         raise click.ClickException(f"🔐 로그인 실패: {res.status_code}\n{res.text}")

#     if not token:
#         token = get_token()

#     headers = {"accept": "*/*", "Authorization": f"Bearer {token}"}

#     url = f"https://aip.sktai.io/api/v1/agent/agents/apps/deployments/{deployment_id}"
#     click.secho(f"🗑️ Deleting deployment: {deployment_id}", fg="red")

#     res = requests.delete(url, headers=headers)
#     if res.status_code in (200, 204):
#         click.secho("✅ Deployment 삭제 완료!", fg="green")
#     else:
#         raise click.ClickException(
#             f"❌ Deployment 삭제 실패: {res.status_code}\n{res.text}"
#         )


# @cli.command(help="🔑 Create API Key for given app_id")
# @click.option("--app-id", required=True, help="Application ID")
# @click.option("--token", default=None, help="Access token (optional)")
# def create_apikey(app_id, token):
#     def get_token():
#         login_url = "https://aip.sktai.io/api/v1/auth/login"
#         login_data = {
#             "grant_type": "",
#             "username": "admin",
#             "password": "aisnb",
#             "scope": "",
#             "client_id": "default",
#             "client_secret": "",
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded",
#             "accept": "application/json",
#         }
#         res = requests.post(login_url, data=login_data, headers=headers)
#         if res.status_code == 201:
#             return res.json().get("access_token")
#         raise click.ClickException(f"🔐 로그인 실패: {res.status_code}\n{res.text}")

#     if not token:
#         token = get_token()

#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

#     url = f"https://aip.sktai.io/api/v1/agent/agents/apps/{app_id}/apikeys"
#     click.secho(f"🔐 Creating API key for App ID: {app_id}", fg="yellow")

#     res = requests.post(url, headers=headers)
#     if res.status_code in (200, 201):
#         click.secho("✅ API 키 생성 완료!", fg="green")
#     else:
#         raise click.ClickException(
#             f"❌ API 키 생성 실패: {res.status_code}\n{res.text}"
#         )


# @cli.command(help="🔍 Get API Keys for given app_id")
# @click.option("--app-id", required=True, help="Application ID")
# @click.option("--token", default=None, help="Access token (optional)")
# def get_apikey(app_id, token):
#     def get_token():
#         login_url = "https://aip.sktai.io/api/v1/auth/login"
#         login_data = {
#             "grant_type": "",
#             "username": "admin",
#             "password": "aisnb",
#             "scope": "",
#             "client_id": "default",
#             "client_secret": "",
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded",
#             "accept": "application/json",
#         }
#         res = requests.post(login_url, data=login_data, headers=headers)
#         if res.status_code == 201:
#             return res.json().get("access_token")
#         raise click.ClickException(f"🔐 로그인 실패: {res.status_code}\n{res.text}")

#     if not token:
#         token = get_token()

#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

#     url = f"https://aip.sktai.io/api/v1/agent/agents/apps/{app_id}/apikeys"
#     click.secho(f"🔍 Getting API Keys for App ID: {app_id}", fg="cyan")

#     res = requests.get(url, headers=headers)
#     if res.status_code == 200:
#         data = res.json().get("data", [])
#         if data:
#             click.secho(f"✅ API 키 목록 ({len(data)}개):", fg="green")
#             for idx, item in enumerate(data, start=1):
#                 click.echo(f"{idx}. {item}")
#         else:
#             click.secho("⚠️ API 키가 없습니다.", fg="yellow")
#     else:
#         raise click.ClickException(
#             f"❌ API 키 조회 실패: {res.status_code}\n{res.text}"
#         )


# # 6. adxp-cli invoke-example
# @cli.command()
# def invoke_example():
#     """예제 API 호출"""
#     try:
#         subprocess.run(["adxp-cli", "invoke-example"], check=True)
#         click.secho("Successfully invoked the example API.", fg="green")
#     except subprocess.CalledProcessError:
#         click.secho("Failed to invoke the example API.", fg="red")
