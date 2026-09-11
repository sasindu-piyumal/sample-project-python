import pytest

from llm_benchmark.datastructures.bst import Tree


@pytest.mark.parametrize("child", [5, 15])
def test_inserting_first_child_updates_root_height(child: int) -> None:
    tree = Tree([10, child])

    assert tree.height == 1
    assert tree.root is not None
    assert tree.root.height == 1
