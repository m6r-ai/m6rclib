"""An embedded compiler for the Metaphor language."""

__version__ = "0.1.0"

# Export main classes so users can import directly from language_parser
from .metaphor_ast_node import MetaphorASTNode, MetaphorASTNodeType
from .metaphor_parser import MetaphorParser, MetaphorParserError

# List what should be available when using `from language_parser import *`
__all__ = [
    "MetaphorASTNode",
    "MetaphorASTNodeType",
    "MetaphorParser",
    "MetaphorParserError",
]
