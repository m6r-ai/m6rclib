# Copyright 2024 M6R Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Types and classes for representing the AST (Abstract Syntax Tree)
of a Metaphor document.
"""

from typing import List, Optional
from enum import IntEnum

class MetaphorASTNodeType(IntEnum):
    """
    Types of nodes that can appear in a Metaphor AST.
    """
    ROOT: int = 0
    TEXT: int = 1
    ROLE: int = 2
    CONTEXT: int = 3
    ACTION: int = 4


class MetaphorASTNode:
    """
    Represents a node in the Abstract Syntax Tree (AST).
    
    Attributes:
        node_type (MetaphorASTNodeType): The type of the token the node represents.
        value (str): The value associated with the node.
    """
    def __init__(self, node_type: MetaphorASTNodeType, value: str) -> None:
        self._node_type: MetaphorASTNodeType = node_type
        self._value: str = value
        self._parent: Optional['MetaphorASTNode'] = None
        self._children: List['MetaphorASTNode'] = []

    def attach_child(self, child: 'MetaphorASTNode') -> None:
        """Add a child node to this MetaphorASTNode."""
        child.parent = self
        self._children.append(child)

    def detach_child(self, child: 'MetaphorASTNode') -> None:
        """Detach a child node from this node in the AST."""
        if child not in self.children:
            raise ValueError("Node is not a child of this node")

        self._children.remove(child)
        child.parent = None

    @property
    def node_type(self) -> MetaphorASTNodeType:
        """The type of this node."""
        return self._node_type

    @property
    def value(self) -> str:
        """The raw text value of this node."""
        return self._value

    @property
    def parent(self) -> Optional['MetaphorASTNode']:
        """The parent node, if any."""
        return self._parent

    @parent.setter
    def parent(self, new_parent: Optional['MetaphorASTNode']) -> None:
        self._parent = new_parent

    @property
    def children(self) -> List['MetaphorASTNode']:
        """The node's children (returns a copy to prevent modification)."""
        return self._children.copy()
