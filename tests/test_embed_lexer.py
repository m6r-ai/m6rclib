import pytest

from m6rclib.embed_lexer import EmbedLexer
from m6rclib.metaphor_token import TokenType

@pytest.fixture
def sample_input():
    return "def hello():\n    print('Hello, World!')"


def test_embed_lexer_creation():
    """Test basic lexer creation"""
    lexer = EmbedLexer("test content", "test.py")
    assert lexer.filename == "test.py"
    assert lexer.input == "test content"
    assert lexer.current_line == 2


def test_embed_lexer_tokenization(sample_input):
    """Test tokenization of Python code"""
    lexer = EmbedLexer(sample_input, "test.py")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert len(tokens) > 0
    assert tokens[0].type == TokenType.TEXT
    assert tokens[0].value.startswith("File:")
    assert "```python" in tokens[1].value


def test_embed_lexer_txt():
    """Test the EmbedLexer's token generation"""
    input_text = "Test content"
    lexer = EmbedLexer(input_text, "test.txt")

    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert len(tokens) == 5
    assert tokens[0].value == "File: test.txt"
    assert tokens[1].value == "```plaintext"
    assert tokens[2].value == "Test content"
    assert tokens[3].value == "```"
    assert tokens[4].type == TokenType.END_OF_FILE


def test_embed_lexer_js():
    """Test the EmbedLexer's token generation"""
    input_text = "Test content"
    lexer = EmbedLexer(input_text, "test.js")

    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert len(tokens) == 5
    assert tokens[0].value == "File: test.js"
    assert tokens[1].value == "```javascript"
    assert tokens[2].value == "Test content"
    assert tokens[3].value == "```"
    assert tokens[4].type == TokenType.END_OF_FILE


def test_embed_lexer_foo_js():
    """Test the EmbedLexer's token generation"""
    input_text = "Test content"
    lexer = EmbedLexer(input_text, "test.foo.js")

    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert len(tokens) == 5
    assert tokens[0].value == "File: test.foo.js"
    assert tokens[1].value == "```javascript"
    assert tokens[2].value == "Test content"
    assert tokens[3].value == "```"
    assert tokens[4].type == TokenType.END_OF_FILE


def test_embed_lexer_m6r():
    """Test the EmbedLexer's token generation"""
    input_text = "Test content"
    lexer = EmbedLexer(input_text, "test.m6r")

    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert len(tokens) == 5
    assert tokens[0].value == "File: test.m6r"
    assert tokens[1].value == "```metaphor"
    assert tokens[2].value == "Test content"
    assert tokens[3].value == "```"
    assert tokens[4].type == TokenType.END_OF_FILE


def test_embed_lexer():
    """Test the EmbedLexer's token generation"""
    input_text = "Test content"
    lexer = EmbedLexer(input_text, "test")

    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert len(tokens) == 5
    assert tokens[0].value == "File: test"
    assert tokens[1].value == "```plaintext"
    assert tokens[2].value == "Test content"
    assert tokens[3].value == "```"
    assert tokens[4].type == TokenType.END_OF_FILE


def test_empty_lexer():
    """Test behavior when all tokens have been consumed"""
    lexer = EmbedLexer("", "test.txt")

    # First consume all regular tokens
    while lexer.tokens:
        lexer.get_next_token()

    # Now get another token when tokens list is empty
    token = lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE
    assert token.value == ""
    assert token.input == ""
    assert token.filename == "test.txt"
    assert token.line == 1
    assert token.column == 1
