"""Tests for the GitHub Action validator script."""

from pathlib import Path

import pytest
import validate as validator

from tests.conftest import tests_data_dir


@pytest.fixture
def mock_workspace(tmp_path: Path, monkeypatch):
    """Workspace for testing."""
    monkeypatch.setattr(validator, "WORKSPACE_PATH", tmp_path)
    return tmp_path


def test_validation_succeeds_with_valid_file(mock_workspace, capsys):
    """Valid file should pass validation."""
    valid_content = (tests_data_dir / "validator" / "positive" / "valid_project.yaml").read_text()
    (mock_workspace / "project.owasp.yaml").write_text(valid_content)

    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 0
    captured = capsys.readouterr()
    assert "SUCCESS: Validation passed!" in captured.out
    assert not captured.err


def test_validation_fails_when_no_file_found(capsys):
    """No file should fail validation."""
    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: OWASP metadata file not found." in captured.err


def test_validation_fails_when_multiple_files_found(mock_workspace, capsys):
    """Multiple files should fail validation."""
    project_content = (
        tests_data_dir / "validator" / "positive" / "valid_project.yaml"
    ).read_text()
    chapter_content = (
        tests_data_dir / "validator" / "positive" / "valid_chapter.yaml"
    ).read_text()

    (mock_workspace / "project.owasp.yaml").write_text(project_content)
    (mock_workspace / "chapter.owasp.yaml").write_text(chapter_content)

    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: Found multiple OWASP metadata files." in captured.err


def test_validation_fails_with_invalid_data(mock_workspace, capsys):
    """Invalid file should fail validation."""
    invalid_content = (
        tests_data_dir / "validator" / "negative" / "invalid_project_type_missing.yaml"
    ).read_text()
    (mock_workspace / "project.owasp.yaml").write_text(invalid_content)

    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: Validation failed!" in captured.err
    assert "'type' is a required property" in captured.err


def test_validation_fails_with_empty_file(mock_workspace, capsys):
    """An empty file should fail validation."""
    empty_content = ""
    (mock_workspace / "project.owasp.yaml").write_text(empty_content)

    with pytest.raises(SystemExit) as exit_info:
        validator.main()  # type: ignore[attr-defined]

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR: Validation failed!" in captured.err
    assert "None is not of type 'object'" in captured.err
