# Changelog for m6rclib

## v0.5.1 (2025-01-15)

Fix a typo in the Metaphor preamble.

## v0.5.0 (2024-11-19)

Made the `MetaphorParserSyntaxError` class public.

Reimplemented all unit tests so they only operate via the public API.

## v0.4.1 (2024-11-17)

Resolve problem in parsing nested "Role:" and "Action:" blocks.

## v0.4.0 (2024-11-17)

Update the "Role:" and "Action:" keywords to allow both to included nested keywords of the same type.

## v0.3.0 (2024-11-14)

Add standard prompt and error formatter functions.

Improve the preamble prompt.

## v0.2.0 (2024-11-13)

This release adds `__str__` and `__repr__` methods to the `MetaphorASTNode` class to simplify debugging and printing.
It also adds a method, `get_children_of_type` that creates a list of all the children of a `MetaphorASTNode` that are
of a given type.

The parsing methods of `MetaphorParser` also now insert a text block preamble that describes Metaphor's syntax, so this
no longer needs to be provided by an application using the library.

## v0.1.1 (2024-11-12)

This release corrects the following problem:

- The Metaphor lexer did not correctly handle Metaphor keywords that appear inside a code fenced block (inside a block
  delimited with 3 backticks).

## v0.1 (2024-11-12)

This is the initial release
