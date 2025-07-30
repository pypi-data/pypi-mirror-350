import sys
import click
import json
import yaml
from typing import TypedDict, Union, List
import os
from pydantic import BaseModel, Field, field_validator
from adxp_sdk.serves.schema import GraphPath


class LanggraphConfig(BaseModel):
    """Defines the structure of graph.yaml file."""

    package_directory: str = Field(
        description="Root Directory of your package(module)."
    )
    graph_path: Union[str, List[GraphPath]] = Field(
        description="Path(s) to the langgraph module.",
        examples=[
            "./react_agent/graph.py:graph",
            [{"name": "first", "object_path": "./react_agent/graph.py:graph"}],
        ],
    )
    env_file: str | None = None
    requirements_file: str | None = None

    @field_validator("graph_path")
    def validate_graph_path(cls, v):
        if isinstance(v, list):
            try:
                for g in v:
                    GraphPath.model_validate(g)
                return v
            except Exception as e:
                raise click.UsageError(
                    f"Invalid graph_path. {v} graph_path는 name과 object_path를 가지고 있어야합니다. : {e}"
                )
        return v


def validate_graph_yaml(graph_yaml: str) -> LanggraphConfig:
    with open(graph_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    try:
        return LanggraphConfig.model_validate(config)
    except Exception as e:
        raise click.UsageError(
            f"Invalid graph.yaml. {graph_yaml} 파일을 확인해주세요. : {e}"
        )
