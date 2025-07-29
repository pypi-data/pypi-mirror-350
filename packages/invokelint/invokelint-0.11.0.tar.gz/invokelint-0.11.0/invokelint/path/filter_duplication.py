"""Filter duplicated paths."""

from typing import List


def _check_subpath(path_a: str, path_b: str) -> int:
    if path_a.startswith(path_b):
        return 1
    if path_b.startswith(path_a):
        return -1
    return 0


def _update_list(path: str, list_filtered: List[str]) -> None:
    for filtered in list_filtered:
        int_subpath = _check_subpath(path, filtered)
        if int_subpath == 1:
            return
        if int_subpath == -1:
            list_filtered.remove(filtered)
            break
    list_filtered.append(path)
    return


def filter_duplication(list_path: List[str]) -> List[str]:
    list_filtered: List[str] = []
    for path in list_path:
        _update_list(path, list_filtered)
    return list_filtered
