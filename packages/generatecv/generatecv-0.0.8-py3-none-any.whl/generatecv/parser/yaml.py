"""YAML Parser for CV Builder.

This module handles the parsing of YAML files containing CV data.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from generatecv.models import CV


def parse_yaml_file(file_path: str) -> dict[str, Any]:
    """Parse a YAML file and return its contents as a dictionary.

    Args:
        file_path: Path to the YAML file

    Returns:
        Dict containing the parsed YAML data

    Raises:
        FileNotFoundError: If the file does not exist
        yaml.YAMLError: If the file cannot be parsed as YAML
    """
    yaml_path = Path(file_path)

    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    try:
        with open(yaml_path, encoding="utf-8") as yaml_file:
            data = yaml.safe_load(yaml_file)
        # Ensure we're returning a dictionary
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict from YAML, got {type(data)}")
        return data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}") from e


def validate_cv_data(data: dict[str, Any]) -> CV:
    """Validates that the CV data is properly structured using Pydantic models.

    Args:
        data: Dictionary containing CV data from YAML

    Returns:
        CV object if data is valid, or a list of validation errors if invalid
    """
    try:
        cv = CV.model_validate(data)
        return cv
    except ValidationError as e:
        raise ValidationError(f"Validation error: {e.errors()}") from e
