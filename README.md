# m6rclib API Documentation

m6rclib is a Python package that provides a parser and prompt compiler for the Metaphor language, a structured text
format for defining roles, contexts, and actions.

## Installation

```bash
pip install m6rclib
```

## Basic Usage

```python
from m6rclib import MetaphorParser

# Create a parser instance
parser = MetaphorParser()

# Parse a Metaphor string
input_text = """
Role:
    You are a helpful assistant.
Context:
    The user needs help with Python.
Action:
    Provide clear Python examples.
"""

# Parse the input with search paths for Include: directives
syntax_tree = parser.parse(input_text, "example.m6r", ["/path/to/includes"])
```

## Core Classes

### MetaphorParser

The main class for parsing Metaphor documents.

#### Methods

- `parse(input_text: str, filename: str, search_paths: List[str]) -> MetaphorASTNode`
  - Parses a string containing Metaphor content
  - Args:
    - `input_text`: The Metaphor content to parse
    - `filename`: Name to use for error reporting
    - `search_paths`: List of paths to search for included files
  - Returns: The root of the abstract syntax tree
  - Raises:
    - `MetaphorParserError`: If there are syntax errors
    - `FileNotFoundError`: If a required file cannot be found

- `parse_file(filename: str, search_paths: List[str]) -> MetaphorASTNode`
  - Parses a Metaphor file
  - Args:
    - `filename`: Path to the file to parse
    - `search_paths`: List of paths to search for included files
  - Returns: The root of the abstract syntax tree
  - Raises:
    - `MetaphorParserError`: If there are syntax errors
    - `FileNotFoundError`: If the file cannot be found

### MetaphorASTNode

Represents a node in the abstract syntax tree (AST).

#### Properties

- `node_type: MetaphorASTNodeType`
  - The type of the node
  - Read-only

- `value: str`
  - The raw text value of the node
  - Read-only

- `parent: Optional[MetaphorASTNode]`
  - The parent node, if any
  - Read-only

- `children: List[MetaphorASTNode]`
  - The node's child nodes (returns a shallow copy)
  - Read-only

#### Methods

- `attach_child(child: MetaphorASTNode) -> None`
  - Adds a child node to this node
  - Args:
    - `child`: The node to attach as a child

- `detach_child(child: MetaphorASTNode) -> None`
  - Removes a child node from this node
  - Args:
    - `child`: The node to detach
  - Raises:
    - `ValueError`: If the node is not a child of this node

- `get_children_of_type(self, node_type: MetaphorASTNodeType) -> List['MetaphorASTNode']`
  - Returns a list of all immediate children that match the specified node type.
  - Args:
    - `node_type (MetaphorASTNodeType)`: The type of nodes to filter for
  - Returns:List of child nodes matching the specified type

### MetaphorASTNodeType

An enumeration of possible AST node types.

#### Values

- `ROOT (0)`: Root node of the AST
- `TEXT (1)`: Text content node
- `ROLE (2)`: Role definition node
- `CONTEXT (3)`: Context definition node
- `ACTION (4)`: Action definition node

### Formatting Functions

Helper functions for formatting nodes and errors.

- `format_ast(node: MetaphorASTNode) -> str`
  - Format an AST node and its children as a string
  - Args:
    - `node`: The root node to format
  - Returns: Formatted string representation of the AST

- `format_errors(errors: List[MetaphorParserSyntaxError]) -> str`
  - Format a list of syntax errors as a string
  - Args:
    - `errors`: List of syntax errors to format
  - Returns: Formatted error string with each error on separate lines

### Exceptions

#### MetaphorParserError

Main exception wrapper for parser errors.

- Attributes:
  - `errors: List[MetaphorParserSyntaxError]`: List of syntax errors encountered

#### MetaphorParserSyntaxError

Detailed syntax error information.

- Attributes:
  - `message: str`: Error description
  - `filename: str`: File where error occurred
  - `line: int`: Line number of error
  - `column: int`: Column number of error
  - `input_text: str`: Input line containing error

## File Format

Metaphor files use the following format:

```metaphor
Role:
    Description of the role
    Additional role details

Context:
    Description of the context
    Context details
    Context: Subsection
        More detailed context information

Action:
    Description of the action
    Step-by-step actions to take
```

### Special Directives

- `Include: filename`
  - Includes another Metaphor file
  - File is searched for in the provided search paths

- `Embed: pattern`
  - Embeds the contents of matching files
  - Supports glob patterns
  - Use `**/` for recursive matching
