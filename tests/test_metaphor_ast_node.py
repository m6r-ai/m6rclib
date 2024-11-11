import pytest

from m6rclib.metaphor_ast_node import MetaphorASTNode, MetaphorASTNodeType

@pytest.fixture
def sample_node():
    return MetaphorASTNode(MetaphorASTNodeType.TEXT, "test input")

def test_metaphor_ast_node_creation(sample_node):
    """Test basic node creation"""
    node = MetaphorASTNode(MetaphorASTNodeType.TEXT, "hello")
    assert node.node_type == MetaphorASTNodeType.TEXT
    assert node.value == "hello"
    assert node.parent is None
    assert len(node.children) == 0

def test_metaphor_ast_node_attach_child(sample_node):
    """Test attaching child nodes"""
    child_node = MetaphorASTNode(MetaphorASTNodeType.TEXT, "child input")

    sample_node.attach_child(child_node)
    assert len(sample_node.children) == 1
    assert child_node.parent == sample_node
    assert sample_node.children[0] == child_node

def test_metaphor_ast_node_detach_child(sample_node):
    """Test detaching a child node"""
    child1_node = MetaphorASTNode(MetaphorASTNodeType.TEXT, "child1")
    child2_node = MetaphorASTNode(MetaphorASTNodeType.TEXT, "child2")

    sample_node.attach_child(child1_node)
    sample_node.attach_child(child2_node)
    assert len(sample_node.children) == 2

    sample_node.detach_child(child1_node)
    assert len(sample_node.children) == 1
    assert(sample_node.children[0].value == "child2")

def test_metaphor_ast_node_detach_unattached_child(sample_node):
    """Test detaching a child node"""
    child1_node = MetaphorASTNode(MetaphorASTNodeType.TEXT, "child1")
    child2_node = MetaphorASTNode(MetaphorASTNodeType.TEXT, "child2")

    sample_node.attach_child(child1_node)
    assert len(sample_node.children) == 1

    with pytest.raises(ValueError) as exc_info:
        sample_node.detach_child(child2_node)

    assert "Node is not a child of this node" in str(exc_info)
