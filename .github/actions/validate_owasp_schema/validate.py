"""Validate schema files against OWASP JSON schema."""

import os
import sys
from pathlib import Path

import yaml

from owasp_schema import get_schema
from owasp_schema.utils.schema_validators import validate_data

SCHEMA_MAP = {
    "chapter.owasp.yaml": "chapter",
    "committee.owasp.yaml": "committee",
    "project.owasp.yaml": "project",
}


def main():
    """Validate a schema file based on its filename."""
    file_path_str = os.environ.get("INPUT_FILE_PATH")
    if not file_path_str:
        sys.stderr.write("Error: Input file path not provided.\n")
        sys.exit(1)

    file_path = Path(file_path_str)
    file_name = file_path.name

    if not file_path.is_file():
        sys.stderr.write(f"Error: File {file_path} does not exist.\n")
        sys.exit(1)

    schema_name = SCHEMA_MAP.get(file_name)
    if not schema_name:
        sys.stderr.write(f"Error: File {file_name} is not a valid schema file.\n")
        sys.exit(1)

    sys.stdout.write(f"Validating {file_name} against {schema_name} schema...\n")

    try:
        schema = get_schema(schema_name)
        with file_path.open("r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError as e:
        sys.stderr.write("Error: " + str(e) + "\n")
        sys.exit(1)

    error_message = validate_data(schema, data)
    if error_message:
        sys.stderr.write(error_message + "\n")
        sys.exit(1)
    else:
        sys.stdout.write("✅ Validation successful.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
