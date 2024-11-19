"""Tests for lexer-related behavior through public API."""

import pytest

from m6rclib import (
    MetaphorASTNodeType,
    MetaphorParser,
    MetaphorParserError,
)


@pytest.fixture
def parser():
    """Provide a parser instance for tests."""
    return MetaphorParser()


def test_empty_input(parser):
    """Test handling of empty input."""
    result = parser.parse("", "test.txt", [])

    # Preamble will still be generated
    assert len(result.children) > 0

    # But no user content
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 0
    assert len(result.get_children_of_type(MetaphorASTNodeType.CONTEXT)) == 0
    assert len(result.get_children_of_type(MetaphorASTNodeType.ACTION)) == 0


def test_indentation_handling(parser):
    """Test handling of indentation through parser."""
    input_text = (
        "Context: Test\n"
        "    Description\n"
        "    Context: Nested\n"
        "        Nested content\n"
    )
    result = parser.parse(input_text, "test.txt", [])
    context_node = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    nested_contexts = context_node.get_children_of_type(MetaphorASTNodeType.CONTEXT)
    assert len(nested_contexts) == 1
    assert len(nested_contexts[0].get_children_of_type(MetaphorASTNodeType.TEXT)) == 1


def test_incorrect_indentation(parser):
    """Test handling of incorrect indentation."""
    input_text = (
        "Role: Test\n"
        "   Bad indent\n"  # 3 spaces instead of 4
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "indent" in error.message.lower()


def test_keyword_handling(parser):
    """Test keyword handling through parser."""
    input_text = (
        "Role: Test\n"
        "    Description\n"
        "Context: Setup\n"
        "    Details\n"
        "Action: Do\n"
        "    Steps\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.CONTEXT)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.ACTION)) == 1


def test_fenced_code_blocks(parser):
    """Test handling of fenced code blocks."""
    input_text = (
        "Context: Test\n"
        "    Before code\n"
        "    ```python\n"
        "    def hello():\n"
        "        print('Hello')\n"
        "    ```\n"
        "    After code\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    context = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    text_nodes = context.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Convert text nodes to list of values for easier testing
    text_values = [node.value for node in text_nodes]
    assert "Before code" in text_values
    assert "```python" in text_values
    assert "def hello():" in text_values
    assert "    print('Hello')" in text_values
    assert "```" in text_values
    assert "After code" in text_values


def test_empty_lines(parser):
    """Test handling of empty lines."""
    input_text = (
        "Role: Test\n"
        "\n"
        "    Description\n"
        "\n"
        "    More text\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    text_nodes = role.get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(text_nodes) == 2
    assert text_nodes[0].value == "Description"
    assert text_nodes[1].value == "More text"


def test_tab_characters(parser):
    """Test handling of tab characters in input."""
    input_text = (
        "Role: Test\n"
        "    Description\n"  # Proper indentation after Role
        "\tTabbed line\n"  # Line starting with tab
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "[Tab]" in error.message


def test_comment_lines(parser):
    """Test handling of comment lines."""
    input_text = (
        "Role: Test\n"
        "    # This is a comment\n"
        "    Actual content\n"
        "# Another comment\n"
        "    More content\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role_node = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    text_nodes = role_node.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Comments should be ignored
    assert len(text_nodes) == 2
    assert text_nodes[0].value == "Actual content"
    assert text_nodes[1].value == "More content"


def test_mixed_spaces_and_tab(parser):
    """Test handling of mixed tabs and spaces."""
    input_text = (
        "Role: Test\n"
        "    First line\n"  # Proper indentation after Role
        "    \t\n"  # Tab preceded by spaces
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "[Tab]" in error.message


def test_tab_in_content_block(parser):
    """Test handling of tabs appearing within a content block."""
    input_text = (
        "Role: Test\n"
        "    Normal line\n"
        "    Line with\ttab\n"  # Tab in middle of content
        "    Another normal line\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role_node = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    text_nodes = role_node.get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(text_nodes) == 3
    assert "\t" in text_nodes[1].value  # Tab preserved in content


def test_commented_keywords(parser):
    """Test that commented keywords are ignored."""
    input_text = (
        "Role: Test\n"
        "    First line\n"
        "# Role: Commented\n"
        "    Second line\n"
        "    # Context: Still commented\n"
        "    Third line\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    # Should only have one Role node since others are commented
    roles = result.get_children_of_type(MetaphorASTNodeType.ROLE)
    assert len(roles) == 1

    # Should have three text lines
    text_nodes = roles[0].get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(text_nodes) == 3
    assert text_nodes[0].value == "First line"
    assert text_nodes[1].value == "Second line"
    assert text_nodes[2].value == "Third line"
