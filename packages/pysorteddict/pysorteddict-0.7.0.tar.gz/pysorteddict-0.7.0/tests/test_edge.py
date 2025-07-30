import pytest

from pysorteddict import SortedDict


@pytest.fixture
def sorted_dict():
    d = SortedDict()
    d[0] = 0
    return d


def test_modify_when_iterators_active(sorted_dict):
    sorted_dict_keys_iters = [iter(sorted_dict.keys()) for _ in range(5)]
    with pytest.raises(RuntimeError, match="^modification not permitted: 5 iterator/iterators is/are alive$"):
        sorted_dict[1] = 1
    with pytest.raises(RuntimeError, match="^modification not permitted: 5 iterator/iterators is/are alive$"):
        sorted_dict.clear()
    for sorted_dict_keys_iter in sorted_dict_keys_iters:
        assert [*sorted_dict_keys_iter]


if __name__ == "__main__":
    pytest.main()
