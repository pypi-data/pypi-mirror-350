from src.helpers.polynomials import PolynomialHelper
import math

class PolynomialToGraphs:
    def __init__(self, l, m):
        self.l = l
        self.m = m
        self.poly_help = PolynomialHelper(l, m)

    def find_min_order(self, value: (int, int)) -> int:
        return int(math.ceil(min(
            self.l / math.gcd(value[0], self.l),
            self.m / math.gcd(value[1], self.m)
        )))

    def find_max_order(self, value: (int, int)) -> int:
        return int(math.ceil(max(
            self.l / math.gcd(value[0], self.l),
            self.m / math.gcd(value[1], self.m)
        )))


    def generate_subgroup(self, generator: (int, int), expression: False) -> list[(int, int)]:
        order = self.find_max_order(generator)
        group = []
        for power in range(1, order + 1):
            my_value = ((generator[0] * power) % self.l, (generator[1] * power) % self.m)
            group.append(my_value)

        if expression:
            return self.poly_help.construct_expression_from_powers(group)
        return group


    def custom_contains(self, generators: list[(int, int)], value: (int, int)) -> bool:
        if len(generators) == 0:
            return False
        if value == (0, 0):
            return True

        value_order = self.find_min_order(value)

        for generator in generators:
            for power in range(1, value_order):
                if (value[0] * power) % self.l == generator[0] and (value[1] * power) % self.m == generator[1]:
                    return True

            generator_order = self.find_min_order(generator)
            for power in range(1, generator_order):
                if (generator[0] * power) % self.l == value[0] and (generator[1] * power) % self.m == value[1]:
                    return True

        return False


    def _remove_duplicate_generators(self, generators: list[(int, int)]) -> list[str]:
        unique: list[(int, int)] = []

        for generator in generators:
            if not self.custom_contains(unique, generator):
                unique.append(generator)

        return self.poly_help.construct_expression_from_powers(unique)


    def find_graph_generators(self, A: list[str], B: list[str], unique = True) -> list[str]:
        generators : list[(int, int)] = []

        for i in range(len(A)):
            for j in range(i + 1, len(A)):
                answer = self.poly_help.multiply_m1_and_m2_inverse(A[i], A[j])
                generators.append(answer)

        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                answer = self.poly_help.multiply_m1_and_m2_inverse(B[i], B[j])
                generators.append(answer)

        if unique:
            return self._remove_duplicate_generators(generators)
        else:
            return self.poly_help.construct_expression_from_powers(generators)


    def is_whole_group_generated(self, generators: list[(int, int)]) -> bool:
        pass

    def group_size(self, generators: list[str]) -> int:
        pass

