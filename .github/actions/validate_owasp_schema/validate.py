"""Validate schema files against OWASP JSON schema."""

import sys
from pathlib import Path

import yaml

from owasp_schema import get_schema
from owasp_schema.utils.schema_validators import validate_data


# The directory inside the Docker container where the user's repository is mounted
REPO_WORKSPACE = Path("/github/workspace")
SCHEMA_MAP = {
    "project.owasp.yaml": "project",
    "chapter.owasp.yaml": "chapter",
    "committee.owasp.yaml": "committee",
}


def main():
    """Automatically finds and validates an OWASP metadata file."""
    sys.stdout.write("Searching for OWASP metadata file...\n")

    found_files = [f for f in SCHEMA_MAP if (REPO_WORKSPACE / f).is_file()]

    if not found_files:
        sys.stderr.write(
            f"No OWASP metadata file found. The repository root \
             must contain one of: {list(SCHEMA_MAP.keys())}\n",
        )
        sys.exit(1)

    if len(found_files) > 1:
        sys.stderr.write(
            f"Multiple OWASP metadata files found: {found_files}. Only one is allowed.\n",
        )
        sys.exit(1)

    file_name = found_files[0]
    file_path = REPO_WORKSPACE / file_name
    schema_name = SCHEMA_MAP[file_name]

    sys.stdout.write(f"Found '{file_name}'. Validating against the '{schema_name}' schema...\n")



    try:
        schema = get_schema(schema_name)
        with file_path.open("r") as f:
            data = yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError) as e:
        sys.stderr.write(
            f"Failed to load schema or YAML file. Details: {e!s}\n",
        )
        sys.exit(1)

    error_message = validate_data(schema=schema, data=data)

    if error_message:
        sys.stderr.write(f"Validation Failed! {error_message}\n")
        sys.exit(1)
    else:
        sys.stdout.write("✅ Validation successful.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
