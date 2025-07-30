from src.helpers.polynomials import PolynomialHelper
from src.helpers.graphs import Category, TannerGraph
from src.core import BBCode

def raw_codes():
    new_codes = {}
    new_codes["0"] = {
        "l": 6,
        "m": 9,
        "A": ["i", "y1", "y2"],
        "B": ["y3", "x2", "x4"],
    }
    new_codes["1"] = {
        "l": 9,
        "m": 9,
        "A": ["i", "x1", "y1"],
        "B": ["x3", "y1", "y2"],
    }
    return new_codes



def display_example(example: dict):
    print(f"l = {example['l']}, m = {example['m']}")
    print(f"A = {example['A']}, B = {example['B']}")


def check_array_equality(a1, a2):
    if len(a1) != len(a2):
        return False
    for element in a1:
        if element not in a2:
            return False
    return True


def check_graph_examples():
    codes = raw_codes()
    for i in range(len(codes)):
        example = codes[str(i)]
        l, m, A, B = example["l"], example["m"], example["A"], example["B"]
        code = BBCode(l, m, A, B)
        G = code.make_graph()

        a, b = G.set_l_and_m(l, m).deconstruct_polynomials(base_node="l0")
        if not check_array_equality(a, A) or not check_array_equality(b, B):
            display_example(example)
            print(f"Obtained code: {a}, {b}")
            exit(1)

        print(f"Code {i} passed.")



if __name__ == "__main__":
    check_graph_examples()


