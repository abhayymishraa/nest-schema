"""Validate schema files against OWASP JSON schema."""

import sys
from pathlib import Path

import yaml

from owasp_schema import get_schema
from owasp_schema.utils.schema_validators import validate_data

# The directory inside the Docker container where the user's repository is mounted
REPO_WORKSPACE = Path("/github/workspace")


def main():
    """Automatically finds and validates an OWASP metadata file."""
    sys.stdout.write("INFO: Searching for OWASP metadata file.")

    found_files = list(REPO_WORKSPACE.glob("*.owasp.yaml"))

    if not found_files:
        sys.stderr.write("ERROR: No OWASP metadata file found.")
        sys.exit(1)

    if len(found_files) > 1:
        sys.stderr.write("ERROR: Multiple OWASP metadata files found.")
        sys.exit(1)

    file_path = found_files[0]
    file_name = file_path.name
    schema_name = file_name.split(".")[0]

    sys.stdout.write(f"INFO: Found '{file_name}'. Validating against the '{schema_name}' schema.")

    schema = get_schema(schema_name)
    with file_path.open("r") as f:
        data = yaml.safe_load(f)

    if error_message := validate_data(schema=schema, data=data):
        sys.stderr.write(f"ERROR: Validation failed! {error_message}")
        sys.exit(1)
    else:
        sys.stdout.write("SUCCESS: Validation successful.")
        sys.exit(0)
