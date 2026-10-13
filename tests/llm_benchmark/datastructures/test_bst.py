from llm_benchmark.datastructures.bst import Tree


def test_tree_height_after_inserts() -> None:
    # 5
    #  \
    #   3
    #    \
    #     1  -> wait, BST order: 3 < 5 goes left, 1 < 3 goes left of 3
    # Path 5 -> 3 -> 1 has 2 edges, so height should be 2.
    tree = Tree([5, 3, 1])

    assert tree.height == 2
    assert tree.height == tree._calculate_height(tree.root)
    assert tree.root.height == 2
