"""An embedded compiler for the Metaphor language."""

__version__ = "0.1.0"

# Export main classes so users can import directly from language_parser
from .ast_node import ASTNode
from .embed_lexer import EmbedLexer
from .metaphor_lexer import MetaphorLexer
from .metaphor_parser import MetaphorParser
from .metaphor_token import Token, TokenType

# List what should be available when using `from language_parser import *`
__all__ = [
    "ASTNode",
    "EmbedLexer",
    "MetaphorLexer",
    "MetaphorParser",
    "Token",
    "TokenType",
]
