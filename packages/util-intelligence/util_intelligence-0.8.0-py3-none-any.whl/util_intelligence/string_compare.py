from typing import Tuple

import numpy as np


def get_levenshtein_distance(src_seq: str, dst_seq: str) -> Tuple[int, str]:
    def get_min_distance_path(matrix: np.ndarray) -> str:
        height, width = matrix.shape
        i, j = height - 1, width - 1
        operations = []
        while i >= 0 or j >= 0:
            if j and matrix[i][j - 1] + 1 == matrix[i][j]:
                operations.append("I")
                j -= 1
                continue
            if i and matrix[i - 1][j] + 1 == matrix[i][j]:
                operations.append("D")
                i -= 1
                continue
            if matrix[i - 1][j - 1] + 1 == matrix[i][j]:
                operations.append("S")
                i -= 1
                j -= 1
                continue
            if matrix[i - 1][j - 1] == matrix[i][j]:
                operations.append("*")
            i -= 1
            j -= 1
        min_path = "".join(operations[::-1])
        return min_path

    def get_min_edit_distance_matrix(src_seq, dst_seq) -> list:
        matrix = [
            [i + j for j in range(len(dst_seq) + 1)]
            for i in range(len(src_seq) + 1)
        ]
        for i in range(1, len(src_seq) + 1):
            for j in range(1, len(dst_seq) + 1):
                d = 0 if src_seq[i - 1] == dst_seq[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + d,
                )
        return matrix

    if src_seq == dst_seq:
        return 0, "*" * len(src_seq)
    else:
        matrix = get_min_edit_distance_matrix(src_seq, dst_seq)
        min_distance = matrix[len(src_seq)][len(dst_seq)]
        min_path = get_min_distance_path(np.array(matrix))
        return min_distance, min_path


def is_circular_equal(a: str, b: str):
    if len(a) > len(b):
        a, b = b, a
    c = a + a
    if b in c:
        return True
    return False
