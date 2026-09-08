"""Correctness tests for Binary Search Tree implementation."""

import pytest

from llm_benchmark.datastructures.bst import Tree, Node


class TestEmptyTreeConstruction:
    """Tests for empty tree construction and initial state."""

    def test_empty_tree_no_arguments(self):
        """Empty tree initialization without arguments."""
        tree = Tree()
        assert tree.root is None
        assert tree.size == 0
        assert tree.height == -1

    def test_empty_tree_none_argument(self):
        """Empty tree initialization with None argument."""
        tree = Tree(None)
        assert tree.root is None
        assert tree.size == 0
        assert tree.height == -1

    def test_empty_tree_empty_list(self):
        """Empty tree initialization with empty list."""
        tree = Tree([])
        assert tree.root is None
        assert tree.size == 0
        assert tree.height == -1


class TestSingleNodeConstruction:
    """Tests for single-node tree construction."""

    def test_single_node_tree_via_list(self):
        """Single-node tree constructed from list."""
        tree = Tree([42])
        assert tree.root is not None
        assert tree.root.value == 42
        assert tree.root.left is None
        assert tree.root.right is None
        assert tree.root.height == 0
        assert tree.size == 1
        assert tree.height == 0

    def test_single_node_tree_via_insert(self):
        """Single-node tree constructed via insertion."""
        tree = Tree()
        tree._insert_value(42)
        assert tree.root is not None
        assert tree.root.value == 42
        assert tree.size == 1
        assert tree.height == 0

    def test_single_node_with_different_types(self):
        """Single-node trees with various value types."""
        for value in [0, -5, 100, "test", 3.14]:
            tree = Tree([value])
            assert tree.root.value == value
            assert tree.size == 1
            assert tree.height == 0


class TestBalancedTreeConstruction:
    """Tests for balanced tree construction and structure."""

    def test_balanced_tree_three_nodes(self):
        """Balanced tree with three nodes: root and two children."""
        tree = Tree([2, 1, 3])
        assert tree.root.value == 2
        assert tree.root.left.value == 1
        assert tree.root.right.value == 3
        assert tree.size == 3
        assert tree.height == 1

    def test_balanced_tree_seven_nodes(self):
        """Perfectly balanced tree with seven nodes."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        # Root should be 4
        assert tree.root.value == 4
        # Level 1: 2, 6
        assert tree.root.left.value == 2
        assert tree.root.right.value == 6
        # Level 2: 1, 3, 5, 7
        assert tree.root.left.left.value == 1
        assert tree.root.left.right.value == 3
        assert tree.root.right.left.value == 5
        assert tree.root.right.right.value == 7
        assert tree.size == 7
        assert tree.height == 2

    def test_balanced_tree_bst_property(self):
        """Balanced tree maintains BST property."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        assert tree._is_valid_bst()


class TestSkewedTreeConstruction:
    """Tests for skewed (unbalanced) tree construction."""

    def test_right_skewed_tree(self):
        """Right-skewed tree from sorted ascending values."""
        tree = Tree([1, 2, 3, 4, 5])
        # Verify structure
        assert tree.root.value == 1
        current = tree.root
        for expected_value in [2, 3, 4, 5]:
            assert current.right.value == expected_value
            assert current.left is None
            current = current.right
        assert tree.size == 5
        assert tree.height == 4

    def test_left_skewed_tree(self):
        """Left-skewed tree from sorted descending values."""
        tree = Tree([5, 4, 3, 2, 1])
        # Verify structure
        assert tree.root.value == 5
        current = tree.root
        for expected_value in [4, 3, 2, 1]:
            assert current.left.value == expected_value
            assert current.right is None
            current = current.left
        assert tree.size == 5
        assert tree.height == 4

    def test_skewed_tree_bst_property(self):
        """Skewed tree maintains BST property."""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree._is_valid_bst()


class TestRecursiveLeftPlacement:
    """Tests for correct recursive placement in left subtree."""

    def test_left_placement_direct_child(self):
        """Value placed as direct left child when < root."""
        tree = Tree([10, 5])
        assert tree.root.left.value == 5
        assert tree.root.right is None

    def test_left_placement_recursive_two_levels(self):
        """Value placed recursively in left subtree (two levels)."""
        tree = Tree([10, 5, 3])
        assert tree.root.value == 10
        assert tree.root.left.value == 5
        assert tree.root.left.left.value == 3
        assert tree.root.left.right is None

    def test_left_placement_recursive_three_levels(self):
        """Value placed recursively in left subtree (three levels)."""
        tree = Tree([10, 5, 3, 1])
        assert tree.root.value == 10
        assert tree.root.left.value == 5
        assert tree.root.left.left.value == 3
        assert tree.root.left.left.left.value == 1

    def test_left_placement_mixed_subtree(self):
        """Left placement with mixed left and right subtrees."""
        tree = Tree([10, 5, 15, 3, 7])
        assert tree.root.value == 10
        assert tree.root.left.value == 5
        assert tree.root.right.value == 15
        assert tree.root.left.left.value == 3
        assert tree.root.left.right.value == 7


class TestRecursiveRightPlacement:
    """Tests for correct recursive placement in right subtree."""

    def test_right_placement_direct_child(self):
        """Value placed as direct right child when > root."""
        tree = Tree([10, 15])
        assert tree.root.right.value == 15
        assert tree.root.left is None

    def test_right_placement_recursive_two_levels(self):
        """Value placed recursively in right subtree (two levels)."""
        tree = Tree([10, 15, 20])
        assert tree.root.value == 10
        assert tree.root.right.value == 15
        assert tree.root.right.right.value == 20
        assert tree.root.right.left is None

    def test_right_placement_recursive_three_levels(self):
        """Value placed recursively in right subtree (three levels)."""
        tree = Tree([10, 15, 20, 25])
        assert tree.root.value == 10
        assert tree.root.right.value == 15
        assert tree.root.right.right.value == 20
        assert tree.root.right.right.right.value == 25

    def test_right_placement_mixed_subtree(self):
        """Right placement with mixed left and right subtrees."""
        tree = Tree([10, 5, 15, 12, 18])
        assert tree.root.value == 10
        assert tree.root.left.value == 5
        assert tree.root.right.value == 15
        assert tree.root.right.left.value == 12
        assert tree.root.right.right.value == 18


class TestDuplicateInsertion:
    """Tests for duplicate value insertion behavior."""

    def test_single_duplicate_no_insertion(self):
        """Duplicate value not inserted, size unchanged."""
        tree = Tree([5, 5])
        assert tree.size == 1
        assert tree.root.value == 5
        assert tree.root.left is None
        assert tree.root.right is None

    def test_multiple_duplicates_no_insertion(self):
        """Multiple duplicates not inserted, size unchanged."""
        tree = Tree([5, 5, 5, 5])
        assert tree.size == 1
        assert tree.root.value == 5

    def test_duplicate_among_distinct_values(self):
        """Duplicate mixed with distinct values."""
        tree = Tree([3, 1, 5, 1, 3, 5])
        assert tree.size == 3
        assert tree.root.value == 3
        assert tree.root.left.value == 1
        assert tree.root.right.value == 5
        assert tree._is_valid_bst()

    def test_duplicate_in_left_subtree(self):
        """Duplicate in left subtree prevents new node."""
        tree = Tree([10, 5, 3, 3])
        assert tree.size == 3
        assert tree.root.left.left.value == 3
        assert tree.root.left.left.left is None
        assert tree.root.left.left.right is None

    def test_duplicate_in_right_subtree(self):
        """Duplicate in right subtree prevents new node."""
        tree = Tree([10, 15, 20, 20])
        assert tree.size == 3
        assert tree.root.right.right.value == 20
        assert tree.root.right.right.left is None
        assert tree.root.right.right.right is None


class TestNodeLinks:
    """Tests for correct node left/right link establishment."""

    def test_node_links_empty_tree(self):
        """Empty tree has no root node."""
        tree = Tree()
        assert tree.root is None

    def test_node_links_single_node(self):
        """Single node has no children."""
        tree = Tree([42])
        node = tree.root
        assert node.left is None
        assert node.right is None

    def test_node_links_both_children(self):
        """Node with both left and right children."""
        tree = Tree([10, 5, 15])
        root = tree.root
        assert root.left is not None
        assert root.right is not None
        assert isinstance(root.left, Node)
        assert isinstance(root.right, Node)
        assert root.left.value == 5
        assert root.right.value == 15

    def test_node_links_only_left_child(self):
        """Node with only left child."""
        tree = Tree([10, 5])
        root = tree.root
        assert root.left is not None
        assert root.right is None

    def test_node_links_only_right_child(self):
        """Node with only right child."""
        tree = Tree([10, 15])
        root = tree.root
        assert root.left is None
        assert root.right is not None

    def test_node_links_complete_tree(self):
        """Node links in a complete tree structure."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        root = tree.root
        # Verify all nodes have correct links
        assert root.left.left.left is None
        assert root.left.left.right is None
        assert root.left.right.left is None
        assert root.left.right.right is None
        assert root.right.left.left is None
        assert root.right.left.right is None
        assert root.right.right.left is None
        assert root.right.right.right is None


class TestSizeVerification:
    """Tests for correct size tracking."""

    def test_size_empty_tree(self):
        """Empty tree has size 0."""
        tree = Tree()
        assert tree.size == 0

    def test_size_single_node(self):
        """Single node has size 1."""
        tree = Tree([42])
        assert tree.size == 1

    def test_size_two_distinct_nodes(self):
        """Two distinct values increase size to 2."""
        tree = Tree([10, 5])
        assert tree.size == 2
        tree = Tree([10, 15])
        assert tree.size == 2

    def test_size_multiple_distinct_insertions(self):
        """Size increases with each distinct insertion."""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree.size == 5

    def test_size_duplicates_no_increase(self):
        """Duplicate insertions do not increase size."""
        tree = Tree([5, 5, 5, 5, 5])
        assert tree.size == 1

    def test_size_mixed_distinct_and_duplicates(self):
        """Size counts only distinct values."""
        tree = Tree([1, 1, 2, 2, 3, 3])
        assert tree.size == 3

    def test_size_after_incremental_insertion(self):
        """Size updates correctly with incremental insertions."""
        tree = Tree()
        for i in range(5):
            tree._insert_value(i)
            assert tree.size == i + 1

    def test_size_incremental_with_duplicates(self):
        """Size stays same when duplicate inserted incrementally."""
        tree = Tree([1])
        assert tree.size == 1
        tree._insert_value(1)
        assert tree.size == 1
        tree._insert_value(2)
        assert tree.size == 2
        tree._insert_value(2)
        assert tree.size == 2


class TestHeightVerification:
    """Tests for correct height tracking."""

    def test_height_empty_tree(self):
        """Empty tree has height -1."""
        tree = Tree()
        assert tree.height == -1

    def test_height_single_node(self):
        """Single node has height 0."""
        tree = Tree([42])
        assert tree.height == 0

    def test_height_node_single_node(self):
        """Single node's height attribute is 0."""
        tree = Tree([42])
        assert tree.root.height == 0

    def test_height_two_nodes_right(self):
        """Two nodes (right child) has height 1."""
        tree = Tree([10, 15])
        assert tree.height == 1
        assert tree.root.height == 1
        assert tree.root.right.height == 0

    def test_height_two_nodes_left(self):
        """Two nodes (left child) has height 1."""
        tree = Tree([10, 5])
        assert tree.height == 1
        assert tree.root.height == 1
        assert tree.root.left.height == 0

    def test_height_three_nodes_balanced(self):
        """Three balanced nodes has height 1."""
        tree = Tree([2, 1, 3])
        assert tree.height == 1
        assert tree.root.height == 1

    def test_height_three_nodes_left_skewed(self):
        """Three left-skewed nodes has height 2."""
        tree = Tree([3, 2, 1])
        assert tree.height == 2
        assert tree.root.height == 2
        assert tree.root.left.height == 1

    def test_height_three_nodes_right_skewed(self):
        """Three right-skewed nodes has height 2."""
        tree = Tree([1, 2, 3])
        assert tree.height == 2
        assert tree.root.height == 2
        assert tree.root.right.height == 1

    def test_height_seven_nodes_balanced(self):
        """Seven balanced nodes has height 2."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        assert tree.height == 2

    def test_height_five_nodes_right_skewed(self):
        """Five right-skewed nodes has height 4."""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree.height == 4
        assert tree.root.height == 4
        assert tree.root.right.height == 3
        assert tree.root.right.right.height == 2
        assert tree.root.right.right.right.height == 1
        assert tree.root.right.right.right.right.height == 0

    def test_height_five_nodes_left_skewed(self):
        """Five left-skewed nodes has height 4."""
        tree = Tree([5, 4, 3, 2, 1])
        assert tree.height == 4
        assert tree.root.height == 4
        assert tree.root.left.height == 3
        assert tree.root.left.left.height == 2
        assert tree.root.left.left.left.height == 1
        assert tree.root.left.left.left.left.height == 0

    def test_height_node_updates_on_insertion(self):
        """Node heights update correctly during recursive insertion."""
        tree = Tree()
        tree._insert_value(10)
        assert tree.root.height == 0
        
        tree._insert_value(5)
        assert tree.root.height == 1
        assert tree.root.left.height == 0
        
        tree._insert_value(15)
        assert tree.root.height == 1
        assert tree.root.left.height == 0
        assert tree.root.right.height == 0
        
        tree._insert_value(3)
        assert tree.root.height == 2
        assert tree.root.left.height == 1
        assert tree.root.left.left.height == 0

    def test_height_with_asymmetric_insertions(self):
        """Heights correctly reflect asymmetric tree structure."""
        tree = Tree([10, 5, 15, 3, 7, 12])
        assert tree.height == 2
        assert tree.root.height == 2
        assert tree.root.left.height == 1
        assert tree.root.right.height == 1
        assert tree.root.left.left.height == 0
        assert tree.root.left.right.height == 0
        assert tree.root.right.left.height == 0


class TestHeightCalculation:
    """Tests for internal height calculation method."""

    def test_calculate_height_none(self):
        """Calculate height of None returns -1."""
        tree = Tree()
        assert tree._calculate_height(None) == -1

    def test_calculate_height_single_node(self):
        """Calculate height of single node returns 0."""
        tree = Tree([42])
        assert tree._calculate_height(tree.root) == 0

    def test_calculate_height_balanced_three_nodes(self):
        """Calculate height of balanced three-node tree."""
        tree = Tree([2, 1, 3])
        assert tree._calculate_height(tree.root) == 1

    def test_calculate_height_skewed_tree(self):
        """Calculate height of skewed tree."""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree._calculate_height(tree.root) == 4

    def test_calculate_height_subtree(self):
        """Calculate height of subtree correctly."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        assert tree._calculate_height(tree.root.left) == 1
        assert tree._calculate_height(tree.root.right) == 1
        assert tree._calculate_height(tree.root.left.left) == 0
        assert tree._calculate_height(tree.root.left.right) == 0


class TestBSTInvariant:
    """Tests for BST invariant maintenance."""

    def test_bst_invariant_empty_tree(self):
        """Empty tree is valid BST."""
        tree = Tree()
        assert tree._is_valid_bst()

    def test_bst_invariant_single_node(self):
        """Single node tree is valid BST."""
        tree = Tree([42])
        assert tree._is_valid_bst()

    def test_bst_invariant_balanced_tree(self):
        """Balanced tree maintains BST property."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        assert tree._is_valid_bst()

    def test_bst_invariant_left_skewed_tree(self):
        """Left-skewed tree maintains BST property."""
        tree = Tree([5, 4, 3, 2, 1])
        assert tree._is_valid_bst()

    def test_bst_invariant_right_skewed_tree(self):
        """Right-skewed tree maintains BST property."""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree._is_valid_bst()

    def test_bst_invariant_with_duplicates_attempt(self):
        """BST remains valid after duplicate insertion attempts."""
        tree = Tree([5, 3, 7, 3, 5, 7])
        assert tree._is_valid_bst()

    def test_bst_invariant_random_order(self):
        """BST maintains property with random insertion order."""
        tree = Tree([50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35])
        assert tree._is_valid_bst()


class TestValidBSTInvariantValidation:
    """Tests for validating correct trees pass invariant checks."""

    def test_valid_invariant_empty_tree(self):
        """Empty tree passes invariant validation."""
        tree = Tree()
        assert tree._is_valid_bst() is True

    def test_valid_invariant_single_node(self):
        """Single node tree passes invariant validation."""
        tree = Tree([5])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_two_nodes_left(self):
        """Two nodes with left child passes invariant."""
        tree = Tree([10, 5])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_two_nodes_right(self):
        """Two nodes with right child passes invariant."""
        tree = Tree([10, 15])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_balanced_three_nodes(self):
        """Balanced three-node tree passes invariant."""
        tree = Tree([10, 5, 15])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_unbalanced_left_three_nodes(self):
        """Unbalanced left-heavy three-node tree passes invariant."""
        tree = Tree([10, 5, 8])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_unbalanced_right_three_nodes(self):
        """Unbalanced right-heavy three-node tree passes invariant."""
        tree = Tree([10, 12, 15])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_seven_node_balanced(self):
        """Seven-node perfectly balanced tree passes invariant."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_right_skewed(self):
        """Right-skewed tree passes invariant."""
        tree = Tree([1, 2, 3, 4, 5, 6, 7])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_left_skewed(self):
        """Left-skewed tree passes invariant."""
        tree = Tree([7, 6, 5, 4, 3, 2, 1])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_large_random_tree(self):
        """Large tree with random insertion order passes invariant."""
        values = [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68, 81, 93]
        tree = Tree(values)
        assert tree._is_valid_bst() is True

    def test_valid_invariant_negative_values(self):
        """Tree with negative values passes invariant."""
        tree = Tree([0, -5, 5, -10, -2, 2, 10])
        assert tree._is_valid_bst() is True

    def test_valid_invariant_with_zero(self):
        """Tree containing zero passes invariant."""
        tree = Tree([0, -1, 1])
        assert tree._is_valid_bst() is True


class TestInvalidBSTInvariantViolations:
    """Tests for detecting BST invariant violations."""

    def test_invalid_invariant_direct_left_violation(self):
        """Directly invalid left child (left value > parent)."""
        tree = Tree([10, 5])
        # Manually corrupt: make left child greater than parent
        tree.root.left.value = 15
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_direct_right_violation(self):
        """Directly invalid right child (right value < parent)."""
        tree = Tree([10, 15])
        # Manually corrupt: make right child less than parent
        tree.root.right.value = 5
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_left_subtree_violation(self):
        """Invalid value in left subtree (violates ancestor bounds)."""
        tree = Tree([10, 5, 3])
        # Manually corrupt: make left-left child exceed parent bound
        tree.root.left.left.value = 12
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_right_subtree_violation(self):
        """Invalid value in right subtree (violates ancestor bounds)."""
        tree = Tree([10, 15, 20])
        # Manually corrupt: make right-right child violate parent bound
        tree.root.right.right.value = 8
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_left_subtree_exceeds_root(self):
        """Left subtree contains value > root (ancestor-bound violation)."""
        tree = Tree([10, 5, 3])
        # Manually corrupt: make deep left node violate root bound
        tree.root.left.left.value = 11
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_right_subtree_below_root(self):
        """Right subtree contains value < root (ancestor-bound violation)."""
        tree = Tree([10, 15, 20])
        # Manually corrupt: make deep right node violate root bound
        tree.root.right.right.value = 9
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_deep_left_violation_three_levels(self):
        """Deep left subtree violation at three levels."""
        tree = Tree([20, 10, 5, 3])
        # Corrupt: make node at depth 3 violate constraint from depth 1
        tree.root.left.left.left.value = 15
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_deep_right_violation_three_levels(self):
        """Deep right subtree violation at three levels."""
        tree = Tree([10, 20, 30, 40])
        # Corrupt: make node at depth 3 violate constraint from depth 1
        tree.root.right.right.right.value = 5
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_middle_subtree_left_bound_violation(self):
        """Middle node in balanced tree violates left bound."""
        tree = Tree([10, 5, 15, 3, 7])
        # Corrupt: make node violate bound from ancestor
        tree.root.left.right.value = 2
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_middle_subtree_right_bound_violation(self):
        """Middle node in balanced tree violates right bound."""
        tree = Tree([10, 5, 15, 12, 18])
        # Corrupt: make node violate bound from ancestor
        tree.root.right.left.value = 20
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_duplicate_left_child(self):
        """Left child with same value as parent."""
        tree = Tree([10, 5])
        # Manually corrupt: make left equal to parent
        tree.root.left.value = 10
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_duplicate_right_child(self):
        """Right child with same value as parent."""
        tree = Tree([10, 15])
        # Manually corrupt: make right equal to parent
        tree.root.right.value = 10
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_swap_two_nodes(self):
        """Two nodes swapped violating BST property."""
        tree = Tree([10, 5, 15])
        # Swap values: now left > root and right < root
        tree.root.left.value = 15
        tree.root.right.value = 5
        assert tree._is_valid_bst() is False

    def test_invalid_invariant_complex_tree_one_violation(self):
        """Complex tree with single node violation."""
        tree = Tree([50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35])
        # Single corruption in middle
        tree.root.left.right.left.value = 60
        assert tree._is_valid_bst() is False


class TestRecursiveHeightCalculation:
    """Tests for recursive height calculation method."""

    def test_calculate_height_none_node(self):
        """Height of None node is -1."""
        tree = Tree()
        assert tree._calculate_height(None) == -1

    def test_calculate_height_leaf_node(self):
        """Height of leaf node is 0."""
        tree = Tree([42])
        assert tree._calculate_height(tree.root) == 0

    def test_calculate_height_two_nodes_left_child(self):
        """Height with only left child."""
        tree = Tree([10, 5])
        assert tree._calculate_height(tree.root) == 1
        assert tree._calculate_height(tree.root.left) == 0

    def test_calculate_height_two_nodes_right_child(self):
        """Height with only right child."""
        tree = Tree([10, 15])
        assert tree._calculate_height(tree.root) == 1
        assert tree._calculate_height(tree.root.right) == 0

    def test_calculate_height_balanced_three_nodes(self):
        """Height of balanced three-node tree."""
        tree = Tree([10, 5, 15])
        assert tree._calculate_height(tree.root) == 1
        assert tree._calculate_height(tree.root.left) == 0
        assert tree._calculate_height(tree.root.right) == 0

    def test_calculate_height_unbalanced_left_three_nodes(self):
        """Height of left-heavy three-node tree."""
        tree = Tree([10, 5, 3])
        assert tree._calculate_height(tree.root) == 2
        assert tree._calculate_height(tree.root.left) == 1
        assert tree._calculate_height(tree.root.left.left) == 0

    def test_calculate_height_unbalanced_right_three_nodes(self):
        """Height of right-heavy three-node tree."""
        tree = Tree([10, 15, 20])
        assert tree._calculate_height(tree.root) == 2
        assert tree._calculate_height(tree.root.right) == 1
        assert tree._calculate_height(tree.root.right.right) == 0

    def test_calculate_height_four_nodes_unbalanced_left(self):
        """Height of four-node left-skewed tree."""
        tree = Tree([10, 5, 3, 1])
        assert tree._calculate_height(tree.root) == 3
        assert tree._calculate_height(tree.root.left) == 2
        assert tree._calculate_height(tree.root.left.left) == 1
        assert tree._calculate_height(tree.root.left.left.left) == 0

    def test_calculate_height_four_nodes_unbalanced_right(self):
        """Height of four-node right-skewed tree."""
        tree = Tree([10, 15, 20, 25])
        assert tree._calculate_height(tree.root) == 3
        assert tree._calculate_height(tree.root.right) == 2
        assert tree._calculate_height(tree.root.right.right) == 1
        assert tree._calculate_height(tree.root.right.right.right) == 0

    def test_calculate_height_seven_nodes_balanced(self):
        """Height of perfectly balanced seven-node tree."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        assert tree._calculate_height(tree.root) == 2
        assert tree._calculate_height(tree.root.left) == 1
        assert tree._calculate_height(tree.root.right) == 1
        assert tree._calculate_height(tree.root.left.left) == 0
        assert tree._calculate_height(tree.root.left.right) == 0
        assert tree._calculate_height(tree.root.right.left) == 0
        assert tree._calculate_height(tree.root.right.right) == 0

    def test_calculate_height_five_nodes_skewed_right(self):
        """Height of five-node right-skewed tree."""
        tree = Tree([1, 2, 3, 4, 5])
        assert tree._calculate_height(tree.root) == 4
        node = tree.root
        for expected_height in [4, 3, 2, 1, 0]:
            assert tree._calculate_height(node) == expected_height
            node = node.right

    def test_calculate_height_five_nodes_skewed_left(self):
        """Height of five-node left-skewed tree."""
        tree = Tree([5, 4, 3, 2, 1])
        assert tree._calculate_height(tree.root) == 4
        node = tree.root
        for expected_height in [4, 3, 2, 1, 0]:
            assert tree._calculate_height(node) == expected_height
            node = node.left

    def test_calculate_height_asymmetric_tree(self):
        """Height calculation for asymmetric tree."""
        tree = Tree([10, 5, 15, 3, 7, 12])
        # Left subtree has height 1, right subtree has height 1
        assert tree._calculate_height(tree.root) == 2
        assert tree._calculate_height(tree.root.left) == 1
        assert tree._calculate_height(tree.root.right) == 1

    def test_calculate_height_complex_tree(self):
        """Height calculation for complex tree."""
        tree = Tree([50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35])
        assert tree._calculate_height(tree.root) == 3

    def test_calculate_height_left_subtree_only(self):
        """Calculate height of subtree with only left children."""
        tree = Tree([10, 5, 3, 1])
        left_subtree = tree.root.left
        assert tree._calculate_height(left_subtree) == 2

    def test_calculate_height_right_subtree_only(self):
        """Calculate height of subtree with only right children."""
        tree = Tree([10, 15, 20, 25])
        right_subtree = tree.root.right
        assert tree._calculate_height(right_subtree) == 2

    def test_calculate_height_single_left_child_only(self):
        """Height when node has only left child (no right)."""
        tree = Tree([10, 5])
        # Root has left child but no right child
        # Height should be 1 + max(-1, 0) = 1
        assert tree._calculate_height(tree.root) == 1

    def test_calculate_height_single_right_child_only(self):
        """Height when node has only right child (no left)."""
        tree = Tree([10, 15])
        # Root has right child but no left child
        # Height should be 1 + max(-1, 0) = 1
        assert tree._calculate_height(tree.root) == 1

    def test_calculate_height_subtree_middle_node(self):
        """Height calculated for middle node in larger tree."""
        tree = Tree([10, 5, 15, 3, 7, 12, 18, 1, 4])
        # Left subtree at root: height 2
        # Right subtree at root: height 1
        # Total root height: 2
        left_middle = tree.root.left
        assert tree._calculate_height(left_middle) == 2

    def test_calculate_height_leaf_subtrees_in_complex_tree(self):
        """Height of leaf nodes in complex tree is always 0."""
        tree = Tree([4, 2, 6, 1, 3, 5, 7])
        # All leaf nodes have height 0
        assert tree._calculate_height(tree.root.left.left) == 0
        assert tree._calculate_height(tree.root.left.right) == 0
        assert tree._calculate_height(tree.root.right.left) == 0
        assert tree._calculate_height(tree.root.right.right) == 0

    def test_calculate_height_consistency_with_tree_height(self):
        """Calculate height on root matches tree height property."""
        values_list = [
            [42],
            [10, 5],
            [10, 15],
            [10, 5, 15],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [4, 2, 6, 1, 3, 5, 7],
        ]
        for values in values_list:
            tree = Tree(values)
            # _calculate_height on root should match tree.height
            calculated = tree._calculate_height(tree.root)
            assert calculated == tree.height
