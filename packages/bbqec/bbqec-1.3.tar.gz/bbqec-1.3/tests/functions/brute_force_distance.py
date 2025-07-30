from src.distances.distance_from_brute_force import generate_all_binary_combinations_bbcode
import numpy as np

def check_binary_combinations_produce_correct_number(n: int) -> bool:
    num_found = 0
    all_operators = generate_all_binary_combinations_bbcode(0, 2 * n, np.zeros(2 * n, dtype=int))
    for operator in all_operators:
            print(operator)
            num_found += 1
    num_expected = int(2 ** (1.5 * n))

    print(f"Number of operators found: {num_found} and expected: {num_expected}")


if __name__ == "__main__":
    num_shots = 10
    for i in range(1, num_shots + 1):
        n = np.random.randint(1, 10)
        if check_binary_combinations_produce_correct_number(n):
            print(f"Example {i} passed")
        else:
            print(f"Example {i} failed")
            print(f"n = {n}")
            exit(1)
