"""Tests for embed functionality through public API."""

import os
from pathlib import Path

import pytest

from m6rclib import (
    MetaphorASTNodeType,
    MetaphorParser,
    MetaphorParserError,
    format_ast,
)


@pytest.fixture
def parser():
    """Provide a parser instance for tests."""
    return MetaphorParser()


@pytest.fixture
def setup_files(tmp_path):
    """Create sample files for testing."""
    # Python file
    py_file = tmp_path / "test.py"
    py_file.write_text("def hello():\n    print('Hello, World!')")

    # Text file
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("Plain text content")

    # JavaScript file
    js_file = tmp_path / "test.js"
    js_file.write_text("function hello() { console.log('Hello'); }")

    # Multiple extension file
    multi_file = tmp_path / "test.spec.js"
    multi_file.write_text("describe('test', () => { it('works', () => {}); });")

    return tmp_path


def test_python_embedding(parser, setup_files):
    """Test embedding of Python files with syntax highlighting."""
    input_text = (
        "Context: Code\n"
        "    Some context\n"
        f"    Embed: {setup_files}/test.py\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    context = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    text_nodes = context.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Find the code block
    code_text = "\n".join(node.value for node in text_nodes)
    assert "```python" in code_text
    assert "def hello():" in code_text
    assert "print('Hello, World!')" in code_text


def test_multiple_file_embedding(parser, setup_files):
    """Test embedding multiple files using wildcards."""
    input_text = (
        "Context: JavaScript\n"
        f"    Embed: {setup_files}/*.js\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    formatted = format_ast(result)

    assert "```javascript" in formatted
    assert "function hello()" in formatted
    assert "describe('test'" in formatted


def test_missing_file_handling(parser, setup_files):
    """Test handling of missing files."""
    input_text = (
        "Context: Missing\n"
        f"    Embed: {setup_files}/nonexistent.txt\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])
    error = exc_info.value.errors[0]
    assert "does not match any files" in error.message


def test_language_detection(parser, setup_files):
    """Test correct language detection for different file types."""
    for filename, expected_lang in [
        ("test.py", "python"),
        ("test.txt", "plaintext"),
        ("test.js", "javascript"),
        ("test.spec.js", "javascript")
    ]:
        input_text = (
            "Context: Test\n"
            f"    Embed: {setup_files}/{filename}\n"
        )

        result = parser.parse(input_text, "test.txt", [])
        formatted = format_ast(result)
        assert f"```{expected_lang}" in formatted


def test_recursive_embedding(tmp_path):
    """Test recursive file embedding with **/ pattern."""
    # Create nested directory structure
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    subsubdir = subdir / "deeper"
    subsubdir.mkdir()

    # Create files at different levels
    (tmp_path / "root.txt").write_text("Root content")
    (subdir / "level1.txt").write_text("Level 1 content")
    (subsubdir / "level2.txt").write_text("Level 2 content")

    parser = MetaphorParser()
    input_text = (
        "Context: Files\n"
        f"    Embed: {tmp_path}/**/*.txt\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    formatted = format_ast(result)

    assert "Root content" in formatted
    assert "Level 1 content" in formatted
    assert "Level 2 content" in formatted


def test_file_without_extension(parser, tmp_path):
    """Test embedding file with no extension."""
    # Create a file without extension
    no_ext_file = tmp_path / "noextension"
    no_ext_file.write_text("Content without extension")

    input_text = (
        "Context: Test\n"
        f"    Embed: {no_ext_file}\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    formatted = format_ast(result)

    # Should use plaintext for files without extension
    assert "```plaintext" in formatted
    assert "Content without extension" in formatted
