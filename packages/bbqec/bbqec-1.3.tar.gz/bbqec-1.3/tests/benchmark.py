from src.core import BBCode
from src.core_optimised import BBCodeOptimised
from src.helpers.parameters import ProposeParameters
import random
import time


def benchmark_cache():
    num_outer_shots = 5
    num_inner_shots = 100
    distance_method = 3

    code_performance = []
    code_cached_performance = []

    for i in range(num_outer_shots):
        l, m = random.randint(9, 22), random.randint(9, 22)
        parameters = ProposeParameters(l, m)
        print(f"l = {l}, m = {m}")
        A_exps = []
        B_exps = []
        for j in range(num_inner_shots):
            A, B = parameters.distribute_monomials(parameters.draw_random_monomials(3, 3))
            A_exps.append(A)
            B_exps.append(B)

        print(f"Benchmarking code cache for l = {l}, m = {m}")
        T1 = time.time()
        code_cached = BBCodeOptimised(l, m)
        for j in range(num_inner_shots):
            A = A_exps[j]
            B = B_exps[j]
            n, k, d = code_cached.set_expressions(A, B).generate_bb_code(distance_method=distance_method)
        T2 = time.time()
        code_cached_performance.append(T2 - T1)


        print(f"Benchmarking code for l = {l}, m = {m}")
        T1 = time.time()
        for j in range(num_inner_shots):
            A = A_exps[j]
            B = B_exps[j]
            code = BBCode(l, m, A, B)
            n, k, d = code.generate_bb_code(distance_method=distance_method)
        T2 = time.time()
        code_performance.append(T2 - T1)

    print("\n\n")
    print(f"caching performance: {code_cached_performance}")
    print(f"code performance: {code_performance}")
    print("\n\n")
    print(f"Total caching performance: {sum(code_cached_performance)}")
    print(f"Total code performance: {sum(code_performance)}")




if __name__ == "__main__":
    benchmark_cache()