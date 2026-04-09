from typing import Optional, List, Any, Tuple


class Node:
    """A node in the Binary Search Tree.
    
    Attributes:
        value: The value stored in this node
        left: Reference to the left child node (None if no left child)
        right: Reference to the right child node (None if no right child)
    """

    def __init__(self, value: Any) -> None:
        """Initialize a Node with a value and no children.
        
        Args:
            value: The value to store in this node
        """
        self.value = value
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None


class Tree:
    """A Binary Search Tree implementation.
    
    Maintains BST invariant: for each node, all values in left subtree < node value < all values in right subtree.
    Tracks size (number of nodes) and height of the tree.
    """

    def __init__(self, values: Optional[List[Any]] = None) -> None:
        """Initialize a Tree with optional initial values.
        
        Args:
            values: Optional list of values to insert into the tree.
                   If None, creates an empty tree.
        """
        self._root: Optional[Node] = None
        self._size: int = 0
        self._height: int = -1  # height of empty tree is -1
        
        if values is not None:
            for value in values:
                self._insert_value(value)
    
    def _insert_value(self, value: Any) -> None:
        """Insert a value into the BST.
        
        Args:
            value: The value to insert
        """
        if self._root is None:
            self._root = Node(value)
            self._size = 1
            self._height = 0
        else:
            inserted, depth = self._insert_recursive(self._root, value, 0)
            if inserted:
                self._size += 1
                if depth > self._height:
                    self._height = depth
    
    def _insert_recursive(self, node: Node, value: Any, depth: int) -> Tuple[bool, int]:
        """Recursively insert a value into the tree.
        
        Args:
            node: Current node in the tree
            value: Value to insert
            depth: Depth of the current node
            
        Returns:
            Tuple (inserted, depth_of_insert):
                - inserted: True if a new node was inserted, False if value already exists
                - depth_of_insert: Depth at which the new node was inserted (undefined if not inserted)
        """
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
                return True, depth + 1
            else:
                return self._insert_recursive(node.left, value, depth + 1)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
                return True, depth + 1
            else:
                return self._insert_recursive(node.right, value, depth + 1)
        else:
            # Duplicate value - don't insert
            return False, depth
    
    @property
    def root(self) -> Optional[Node]:
        """Get the root node of the tree (read-only).
        
        Returns:
            The root Node, or None if tree is empty
        """
        return self._root
    
    @property
    def size(self) -> int:
        """Get the number of nodes in the tree (read-only).
        
        Returns:
            The count of nodes in the tree
        """
        return self._size
    
    @property
    def height(self) -> int:
        """Get the height of the tree (read-only).
        
        Returns:
            The height of the tree (-1 for empty tree, 0 for single node, etc.)
        """
        return self._height
    
    def _is_valid_bst(self) -> bool:
        """Verify that the tree satisfies BST invariants.
        
        BST invariant: For each node, all values in the left subtree are less than
        the node's value, and all values in the right subtree are greater than
        the node's value.
        
        Returns:
            True if the tree is a valid BST, False otherwise
        """
        def is_valid_bst_recursive(node: Optional[Node], min_value: Any = None, max_value: Any = None) -> bool:
            """Helper function to validate BST properties recursively.
            
            Args:
                node: Current node being validated
                min_value: Minimum value this node's value must exceed (or None)
                max_value: Maximum value this node's value must not exceed (or None)
                
            Returns:
                True if this subtree is a valid BST, False otherwise
            """
            if node is None:
                return True
            
            # Check if current node violates constraints
            if min_value is not None and node.value <= min_value:
                return False
            if max_value is not None and node.value >= max_value:
                return False
            
            # Recursively validate left and right subtrees
            return (is_valid_bst_recursive(node.left, min_value, node.value) and
                    is_valid_bst_recursive(node.right, node.value, max_value))
        
        return is_valid_bst_recursive(self._root)
    
    def _calculate_height(self, node: Optional[Node]) -> int:
        """Calculate the height of a subtree rooted at the given node.
        
        Height is defined as the number of edges from the node to the deepest leaf.
        Empty tree (None) has height -1.
        A single node has height 0.
        
        Args:
            node: The root of the subtree to measure
            
        Returns:
            The height of the subtree (-1 for None, 0 for leaf node, etc.)
        """
        if node is None:
            return -1
        
        left_height = self._calculate_height(node.left)
        right_height = self._calculate_height(node.right)
        
        return 1 + max(left_height, right_height)