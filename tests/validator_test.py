"""Tests for the GitHub Action validator script."""

from pathlib import Path

import pytest
import validate as validator


@pytest.fixture
def mock_workspace(tmp_path: Path, monkeypatch):
    """Workspace for testing."""
    monkeypatch.setattr(validator, "WORKSPACE_PATH", tmp_path)
    return tmp_path


def test_validation_succeeds_with_valid_file(mock_workspace, capsys):
    """Valid file should pass validation."""
    valid_content = """
                    name: OWASP Incubator Code Project
                    level: 2
                    type: code
                    pitch: "A very brief, one-line description of your project"

                    audience:
                      - breaker

                    leaders:
                      - name: Leader 1 Name
                        github: leader-1-github
                      - name: Leader 2 Name
                        github: leader-2-github
                        slack: leader-2-slack
                    """
    (mock_workspace / "project.owasp.yaml").write_text(valid_content)

    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 0

    captured = capsys.readouterr()
    assert "SUCCESS: Validation passed!" in captured.out
    assert captured.err == ""


def test_validation_fails_when_no_file_found(capsys):
    """No file should fail validation."""
    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: OWASP metadata file not found." in captured.err


def test_validation_fails_when_multiple_files_found(mock_workspace, capsys):
    """Multiple files should fail validation."""
    (mock_workspace / "project.owasp.yaml").touch()
    (mock_workspace / "chapter.owasp.yaml").touch()

    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: Found multiple OWASP metadata files." in captured.err


def test_validation_fails_with_invalid_data(mock_workspace, capsys):
    """Invalid file should fail validation."""
    invalid_content = """
                      audience:
                        - breaker
                      leaders:
                        - github: leader-1-github
                          name: Leader 1 Name
                        - github: leader-2-github
                          name: Leader 2 Name
                          slack: leader-2-slack
                      level: 2
                      name: OWASP Incubator Code Project
                      pitch: A very brief, one-line description of your project
                      tags:
                        - example-tag-1
                        - example-tag-2
                        - example-tag-3
                      """
    (mock_workspace / "project.owasp.yaml").write_text(invalid_content)
    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: Validation failed!" in captured.err
    assert "'type' is a required property" in captured.err
