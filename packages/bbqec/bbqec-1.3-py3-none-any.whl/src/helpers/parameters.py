import numpy as np
import random
import math

class ProposeParameters:
    def __init__(self, l: int, m: int):
        self.l = l
        self.m = m
        self.validate_input()


    def validate_input(self):
        if not 1 <= self.l <= 100:
            raise ValueError("l should be between 1 and 100")
        if not 1 <= self.m <= 100:
            raise ValueError("m should be between 1 and 100")
        pass

    @staticmethod
    def distribute_monomials(all_monomials: list[str], num_A: int = None):
        num_monomials = len(all_monomials)
        if num_A is None:
            num_A = num_monomials // 2

        A = all_monomials[:num_A]
        B = all_monomials[num_A:]
        return A, B

    def redraw_l_m_from_normal_distribution(self, change_with_probability: float = 0.01, std_dev_power: float = 0.5):
        a = np.random.random()
        if a < change_with_probability:
            new_l = np.random.normal(self.l, self.l ** std_dev_power)
            new_m = np.random.normal(self.m, self.m ** std_dev_power)
            if 1 <= new_l <= 40 and 1 <= new_m <= 40:
                self.l = int(new_l)
                self.m = int(new_m)
                return True
        return False

    def draw_bivariate_monomials(self, num_monomials: int = 3):
        monomial_indices = np.random.choice(self.l * self.m, num_monomials, replace=False, p=None)
        x_exponents = monomial_indices // self.m
        y_exponents = monomial_indices % self.m
        monomials = [f"x{i}.y{j}" for i, j in zip(x_exponents, y_exponents)]
        return monomials

    def draw_random_monomials(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        x_exponents = np.random.choice(self.l, num_x_monomials, replace=False, p=None)
        y_exponents = np.random.choice(self.m, num_y_monomials, replace=False, p=None)
        monomials = [f"x{i}" for i in x_exponents] + [f"y{i}" for i in y_exponents]
        random.shuffle(monomials)
        return monomials


    def draw_disconnected_monomials(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        x_candidates = [i for i in range(1, self.l) if math.gcd(i, self.l) != 1]
        y_candidates = [i for i in range(1, self.m) if math.gcd(i, self.m) != 1]
        x_exponents = np.random.choice(x_candidates, num_x_monomials, replace=False, p=None)
        y_exponents = np.random.choice(y_candidates, num_y_monomials, replace=False, p=None)
        monomials = [f"x{i}" for i in x_exponents] + [f"y{i}" for i in y_exponents]
        random.shuffle(monomials)
        return monomials

    def draw_odd_exponents_monomials(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        x_candidates = [i for i in range(1, self.l, 2)]
        y_candidates = [i for i in range(1, self.m, 2)]
        x_exponents = np.random.choice(x_candidates, num_x_monomials, replace=False, p=None)
        y_exponents = np.random.choice(y_candidates, num_y_monomials, replace=False, p=None)
        monomials = [f"x{i}" for i in x_exponents] + [f"y{i}" for i in y_exponents]
        random.shuffle(monomials)
        return monomials

    def change_one_monomial(self, monomial_expression: list[str], index: int):
        variable, exp = monomial_expression[index][0], int(monomial_expression[index][1:])
        if variable == "x":
            if exp + 1 < self.l:
                monomial_expression[index] = f"x{exp + 1}"
            else:
                monomial_expression[index] = f"x0"
        else:
            if exp + 1 < self.m:
                monomial_expression[index] = f"y{exp + 1}"
            else:
                monomial_expression[index] = f"y0"

        return monomial_expression


    def create_initial_input_parameters(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        if num_x_monomials > self.l or num_y_monomials > self.m:
            raise ValueError("Number of monomials cannot be greater than l or m")

        all_monomials = self.draw_random_monomials(num_x_monomials, num_y_monomials)
        A, B = self.distribute_monomials(all_monomials)
        return {
            "l" : self.l,
            "m" : self.m,
            "a" : A,
            "b" : B
        }




if __name__ == "__main__":
    propose = ProposeParameters(12, 12)
    for i in range(10):
        print(propose.draw_bivariate_monomials(4))