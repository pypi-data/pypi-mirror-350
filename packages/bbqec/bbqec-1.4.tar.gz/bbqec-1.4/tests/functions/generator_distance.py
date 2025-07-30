import numpy as np
from src.distances.distance_from_generators import generate_binary_combinations_for_generators


def check_binary_combinations_produce_right_number_of_operators(n: int, k: int) -> bool:
    num_found = 0
    all_operators = generate_binary_combinations_for_generators(0, n + k, n - k, np.zeros(n + k, dtype=int))
    for _ in all_operators:
            num_found += 1
    num_expected = 2 ** (n + k) -  2 ** (n - k)
    return num_found == num_expected



if __name__ == "__main__":
    num_shots = 10
    for i in range(1, num_shots + 1):
        n = np.random.randint(1, 10)
        k = np.random.randint(1, 10)
        if check_binary_combinations_produce_right_number_of_operators(n, k):
            print(f"Example {i} passed")
        else:
            print(f"Example {i} failed")
            print(f"n = {n}, k = {k}")
            exit(1)

