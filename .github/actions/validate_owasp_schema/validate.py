import sys
from pathlib import Path
import yaml
from owasp_schema import get_schema
from owasp_schema.utils.schema_validators import validate_data

# The directory inside the Docker container where the user's repository is mounted.
REPO_WORKSPACE = Path("/github/workspace")

# A mapping from filename to the schema name required by the `owasp-schema` package.
SCHEMA_MAP = {
    "project.owasp.yaml": "project",
    "chapter.owasp.yaml": "chapter",
    "committee.owasp.yaml": "committee",
}

def main():
    """
    Automatically finds and validates an OWASP metadata file
    in the root of a checked-out repository.
    """
    sys.stdout.write("Searching for OWASP metadata file...\n")

    # 1. Find which of the target files exist in the root of the repository.
    found_files = [f for f in SCHEMA_MAP.keys() if (REPO_WORKSPACE / f).is_file()]

    # 2. Handle cases where zero or multiple files are found.
    if not found_files:
        sys.stderr.write(f"::error::No OWASP metadata file found. The repository root must contain one of: {list(SCHEMA_MAP.keys())}\n")
        sys.exit(1)

    if len(found_files) > 1:
        sys.stderr.write(f"::error::Multiple OWASP metadata files found: {found_files}. Only one is allowed.\n")
        sys.exit(1)

    # 3. If we get here, exactly one file was found.
    file_name = found_files[0]
    file_path = REPO_WORKSPACE / file_name
    schema_name = SCHEMA_MAP[file_name]

    sys.stdout.write(f"Found '{file_name}'. Validating against the '{schema_name}' schema...\n")

    # 4. Load the schema and the YAML data file.
    try:
        schema = get_schema(schema_name)
        with file_path.open("r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        # Using "file=" helps GitHub link the error to the specific file.
        sys.stderr.write(f"::error file={file_name}::Failed to load schema or YAML file. Details: {str(e)}\n")
        sys.exit(1)

    # 5. Validate the data against the schema.
    error_message = validate_data(schema=schema, data=data)

    # 6. Report the final result using your requested style.
    if error_message:
        sys.stderr.write(f"::error file={file_name}::Validation Failed! {error_message}\n")
        sys.exit(1)
    else:
        # Use the exact success message you wanted.
        sys.stdout.write("✅ Validation successful.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()