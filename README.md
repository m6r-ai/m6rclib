# User manual for the m6rc Metaphor compiler library

## Introduction

The m6rc compiler library is an embedded library designed to parse, simplify, and process Metaphor language code.
This document outlines its usage and functionality.

## What is Metaphor?

Metaphor is a simple language designed to create Large Context Prompts (LCPs) for Large Language Models (LLMs).

Metaphor follows a very simple design that captures an action objective for the LLM to fulfil.  This action is supported by a
hierarchical description of the context the LLM is being asked to use to fulfil the action.

The design is natural language based but this use of natural language is slightly constrained by some keywords so m6rc can
construct more effective LCP prompts.

This approach has many advantages:

- We can iterate from a simple description to a more complex one over time.
- When using this to build software, we can quickly iterate new versions, allowing us to try out new ideas very rapidly,
  prior to committing to them.
- This approach captures the "memory" of what we're trying to achieve in the prompt as opposed to in an interactive dialogue
  with an LLM.  This means we can use the same approach with different LLMs, and can take advantage of "temporary" sessions
  with an LLM so that we don't contaminate the LLM's output based on previous experiments that may not have been fully
  successful.

### Syntax

Metaphor (m6r) files follow a very simple document-like structure.  It has only 5 keywords:

- `Action:` - defines the top-level action objective being conveyed to the LLM.  There is only one `Action:` keyword
  in any given Metaphor input.
- `Context:` - a hierarchical description of the context of the work we want the LLM to do and supporting information.
- `Embed:` - embeds an external file into the prompt, also indicating the language involved to the LLM.
- `Include:` - includes another Metaphor file into the current one, as if that one was directly part of the file being
  procesed, but auto-indented to the current indentation level.
- `Role:` - defines a role to be played by the LLM (optional).

A Metaphor description requires an `Action:` block and a `Context:` block.  `Context:` blocks are nested to provide
detail.  Here is a very simple example:

```
Context: Top-level context
    Some notes about the top-level context

    Context: More context to support the top-level context
        Description of the extra context

Action:
    Some instructions..
```

### Indentation

To avoid arguments over indentation, Metaphor supports only one valid indentation strategy.  All nested items must be
indented by exactly 4 spaces.

Tab characters may be used inside embedded files, but must not be used to indent elements inside Metaphor files.

## Error messages

The compiler provides clear and detailed error messages if issues are detected during the parsing process.
Errors typically include:

- A description of the error
- Line number
- Column number
- File name

For example:

```
Expected 'Action' keyword: line 10, column 5, file example.m6r
```

## FAQ

### Why `m6r`?

m6r is short for Metaphor (m, 6 letters, r).  It's quicker and easier to type!
