from typing import List, Optional

import pytest

from llm_benchmark.datastructures.bst import Node, Tree


class TestNode:
    """Tests for the Node class"""

    def test_node_creation(self) -> None:
        """Test that a node can be created with a value"""
        node = Node(5)
        assert node.value == 5
        assert node.left is None
        assert node.right is None

    def test_node_with_different_types(self) -> None:
        """Test that a node can hold different value types"""
        node_int = Node(10)
        assert node_int.value == 10

        node_str = Node("hello")
        assert node_str.value == "hello"

        node_float = Node(3.14)
        assert node_float.value == 3.14


class TestTreeEmpty:
    """Tests for empty Tree"""

    def test_empty_tree_creation(self) -> None:
        """Test creating an empty tree"""
        tree = Tree()
        assert tree.root is None
        assert tree.size == 0
        assert tree.height == -1

    def test_empty_tree_is_valid_bst(self) -> None:
        """Test that an empty tree is a valid BST"""
        tree = Tree()
        assert tree._is_valid_bst()


class TestTreeSingleNode:
    """Tests for Tree with a single node"""

    def test_single_node_tree(self) -> None:
        """Test creating a tree with a single value"""
        tree = Tree([5])
        assert tree.root is not None
        assert tree.root.value == 5
        assert tree.size == 1
        assert tree.height == 0

    def test_single_node_is_valid_bst(self) -> None:
        """Test that a single node tree is a valid BST"""
        tree = Tree([5])
        assert tree._is_valid_bst()


class TestTreeInsertion:
    """Tests for Tree insertion"""

    def test_insert_multiple_values(self) -> None:
        """Test inserting multiple values"""
        tree = Tree([5, 3, 7, 2, 4, 6, 8])
        assert tree.size == 7
        assert tree.root.value == 5
        assert tree.root.left.value == 3
        assert tree.root.right.value == 7

    def test_insert_left_only(self) -> None:
        """Test inserting values that go only left"""
        tree = Tree([5, 4, 3, 2, 1])
        assert tree.size == 5
        assert tree.root.value == 5
        assert tree.root.left.value == 4
        assert tree.root.left.left.value == 3

    def test_insert_right_only(self) -> None:
        """Test inserting values that go only right"""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree.size == 5
        assert tree.root.value == 1
        assert tree.root.right.value == 2
        assert tree.root.right.right.value == 3

    def test_duplicate_not_inserted(self) -> None:
        """Test that duplicate values are not inserted"""
        tree = Tree([5, 3, 7, 3, 5, 7])
        assert tree.size == 3
        assert tree.root.value == 5
        assert tree.root.left.value == 3
        assert tree.root.right.value == 7

    @pytest.mark.parametrize(
        "values, expected_size",
        [
            ([5], 1),
            ([5, 3], 2),
            ([5, 3, 7], 3),
            ([5, 3, 7, 2, 4], 5),
            ([1, 2, 3, 4, 5], 5),
        ],
    )
    def test_tree_size(self, values: List[int], expected_size: int) -> None:
        """Test that tree size is correct"""
        tree = Tree(values)
        assert tree.size == expected_size


class TestTreeHeight:
    """Tests for Tree height calculation"""

    def test_height_single_node(self) -> None:
        """Test height of single node tree"""
        tree = Tree([5])
        assert tree.height == 0

    def test_height_balanced_tree(self) -> None:
        """Test height of a balanced tree"""
        tree = Tree([5, 3, 7])
        assert tree.height == 1

    def test_height_left_skewed(self) -> None:
        """Test height of a left-skewed tree"""
        tree = Tree([5, 4, 3, 2, 1])
        assert tree.height == 4

    def test_height_right_skewed(self) -> None:
        """Test height of a right-skewed tree"""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree.height == 4

    @pytest.mark.parametrize(
        "values, expected_height",
        [
            ([5], 0),
            ([5, 3, 7], 1),
            ([5, 3, 7, 2, 4, 6, 8], 2),
            ([1, 2, 3, 4, 5], 4),
        ],
    )
    def test_tree_height_parametrized(self, values: List[int], expected_height: int) -> None:
        """Test tree height with parametrized inputs"""
        tree = Tree(values)
        assert tree.height == expected_height


class TestTreeBSTProperty:
    """Tests for BST property validation"""

    def test_balanced_tree_is_valid_bst(self) -> None:
        """Test that a balanced tree satisfies BST property"""
        tree = Tree([5, 3, 7, 2, 4, 6, 8])
        assert tree._is_valid_bst()

    def test_left_skewed_is_valid_bst(self) -> None:
        """Test that a left-skewed tree satisfies BST property"""
        tree = Tree([5, 4, 3, 2, 1])
        assert tree._is_valid_bst()

    def test_right_skewed_is_valid_bst(self) -> None:
        """Test that a right-skewed tree satisfies BST property"""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree._is_valid_bst()

    def test_single_value_is_valid_bst(self) -> None:
        """Test that a single value tree satisfies BST property"""
        tree = Tree([42])
        assert tree._is_valid_bst()


def test_benchmark_tree_creation(benchmark) -> None:
    """Benchmark tree creation with multiple values"""
    benchmark(Tree, [50, 30, 70, 20, 40, 60, 80])


def test_benchmark_large_tree_creation(benchmark) -> None:
    """Benchmark tree creation with larger dataset"""
    values = list(range(1, 101))
    benchmark(Tree, values)
