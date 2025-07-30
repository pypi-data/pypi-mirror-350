from sage.all import PolynomialRing, GF
from src.helpers.polynomials import PolynomialHelper


class BivariatePolynomialHelper:
    def __init__(self, l: int, m: int):
        self.l = l
        self.m = m
        self.poly_help = PolynomialHelper(l, m)

    def factorize_bivariate(self, polynomial: list[str]) -> (list[str], list[int]):
        polynomials_powers = self.poly_help.construct_powers_from_expression(polynomial)
        factors, factor_powers = sage_factorization(polynomials_powers)

        answer = []
        answer_exp = []
        for factor, power in zip(factors, factor_powers):
            values = factor.split(" + ")
            if len(values) == 1:
                continue
            values = [v.replace("^","").replace("*", ".") for v in values]
            values = [self.poly_help._construct_expression(*self.poly_help._construct_powers(v)) for v in values]
            answer.append(values)
            answer_exp.append(power)
        return answer, factor_powers



def sage_factorization(polynomial_powers: list[(int, int)]) -> (list[str], list[int]):
    ring = PolynomialRing(GF(2), ['x', 'y'])
    x, y = ring.gens()

    p = 0
    for power in polynomial_powers:
        p += (x ** power[0]) * (y ** power[1])
    factors = p.factor()

    answer: list[str] = []
    answer_exp: list[int] = []
    for factor, multiplicity in factors:
        answer.append(str(factor))
        answer_exp.append(int(multiplicity))
    return answer, answer_exp

