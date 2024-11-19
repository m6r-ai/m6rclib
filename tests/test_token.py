"""Tests for token-like behavior through the parser's public API."""

import pytest

from m6rclib import (
    MetaphorASTNodeType,
    MetaphorParser,
    MetaphorParserError,
    MetaphorParserSyntaxError,
)


@pytest.fixture
def parser():
    """Provide a parser instance for tests."""
    return MetaphorParser()


def test_valid_keyword_parsing(parser):
    """Test that valid keywords are parsed correctly."""
    input_text = (
        "Role: Test\n"
        "    Description\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    roles = result.get_children_of_type(MetaphorASTNodeType.ROLE)
    assert len(roles) == 1
    assert roles[0].value == "Test"


def test_invalid_keyword_error(parser):
    """Test that invalid keywords raise appropriate error."""
    input_text = "InvalidKeyword: Test\n    Text\n"

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "Unexpected token" in error.message


def test_error_location_tracking(parser):
    """Test that error location is correctly tracked."""
    input_text = (
        "Role: Test\n"
        "    Description\n"
        "  BadIndent: Wrong\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert error.line == 3
    assert "test.txt" == error.filename


def test_keyword_empty_value(parser):
    """Test parsing keyword with no value."""
    input_text = (
        "Role:\n"
        "    Description\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    assert role.value == ""


def test_keyword_whitespace_value(parser):
    """Test parsing keyword with whitespace value."""
    input_text = (
        "Role:     \n"
        "    Description\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    assert role.value == ""


def test_duplicate_role_error(parser):
    """Test that duplicate Role keywords raise error."""
    input_text = (
        "Role: First\n"
        "    Description\n"
        "Role: Second\n"
        "    Text\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "'Role' already defined" in error.message


def test_duplicate_context_error(parser):
    """Test that duplicate Context keywords raise error."""
    input_text = (
        "Context: First\n"
        "    Description\n"
        "Context: Second\n"
        "    Text\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "'Context' already defined" in error.message


def test_duplicate_action_error(parser):
    """Test that duplicate Action keywords raise error."""
    input_text = (
        "Action: First\n"
        "    Description\n"
        "Action: Second\n"
        "    Text\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "'Action' already defined" in error.message


def test_keyword_text_preservation(parser):
    """Test that text following keywords is preserved."""
    input_text = (
        "Role: Test Role Description\n"
        "    Text\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    assert role.value == "Test Role Description"


def test_text_content_preservation(parser):
    """Test that indented text content is preserved."""
    input_text = (
        "Role: Test\n"
        "    First line\n"
        "    Second line\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    texts = role.get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(texts) == 2
    assert texts[0].value == "First line"
    assert texts[1].value == "Second line"
