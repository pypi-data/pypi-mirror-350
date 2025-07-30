import numpy as np
import src.helpers.linalg_helpers as linalg_help


# Find all possible combinations of logical operators, multiplied by stabilizers
def generate_binary_combinations_for_generators(i:int, num_bits:int, num_stabilizers: int, arr) -> np.ndarray:
    if i == num_bits:
        if sum(arr[num_stabilizers:]) == 0:
            return
        else:
            yield arr
            return

    arr[i] = 0
    yield from generate_binary_combinations_for_generators(i + 1, num_bits, num_stabilizers, arr)
    arr[i] = 1
    yield from generate_binary_combinations_for_generators(i + 1, num_bits, num_stabilizers, arr)



def calculate_distance(H_x, H_z, n:int, k: int, status_updates=False):
    # refer Neilson and Chuang, Chapter 10, Eq. 10.111
    #
    #   column size = rank_x | n - k - rank_x | k
    #
    # G_standard    = [ I A1 A2 | B 0 C ]       size = rank_x
    #                 [ 0 0  0  | D I E ]       size = n - k - rank_x ( = rank_z)
    #
    # For BB codes, rank_x = rank_z

    rank_x = linalg_help.binary_rank(H_x)

    G_standard = linalg_help.standard_form(H_x, H_z)
    Lx, Lz = linalg_help.find_logical_generators(G_standard, rank_x)

    complete_matrix = np.vstack((G_standard, Lx, Lz))

    all_permutations = generate_binary_combinations_for_generators(0, n + k, n - k, np.zeros(n + k, dtype=int))
    min_distance = 2 * n

    c = 0
    if status_updates:
        print(f"\nFinding all logical operators. Checking : {2 ** (n + k) - 2 ** (n - k)} operators.")

    for perm in all_permutations:

        if c % 100000 == 0 and status_updates:
            print(f"Checked {c} operators")
        c += 1

        product = np.zeros((2 * n), dtype=int)
        for index, value in enumerate(perm):
            if value == 1:
                product = [(product[j] + complete_matrix[index][j]) % 2 for j in range(2 * n)]

        min_distance = min(min_distance, linalg_help.hamming_weight(product))

    if status_updates:
        print(f"Checked {c} operators. \nSearch complete.\n")

    return min_distance












