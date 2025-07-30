from src.core import BBCode
import os
import json

def check_custom_codes(codes: dict):
    codes["0"] = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [108, 16, 6]
    }
    codes["1"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "x1", "y1"],
        "b": ["x3", "y1", "y2"],
        "answer": [162, 4, 16]
    }


def display_code(example: dict, n: int, k: int, d: int):
    print("Code Failed.")
    print(f"l = {example['l']}, m = {example['m']}")
    print(f"A = {example['a']}, B = {example['b']}")
    print(f"Obtained code: [{n}, {k}, {d}]")
    print(f"Known code: {example['answer']}")
    return


def run_bbcode_examples(distance_method, distance_margin, custom_codes):
    Main = {}

    if custom_codes:
        check_custom_codes(Main)
    else:
        folder_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(folder_path, "known_codes")

        with open(file_path, "r") as file:
            json_readable = file.read().replace("\'", "\"")
            Main = json.loads(json_readable)

    for i in range(len(Main)):
        example = Main[str(i)]
        code = BBCode(example["l"], example["m"], example["a"], example["b"])

        n, k, d = code.generate_bb_code(distance_method=distance_method)
        n_known, k_known, d_known = example["answer"]

        passed = n == n_known and k == k_known and d_known <= d * distance_margin

        if not passed:
            display_code(example, n, k, d)
            exit(1)

        print(f"Code {i} passed.")


if __name__ == "__main__":
    distance_method = 3
    distance_margin = 1.15
    custom_codes = False
    run_bbcode_examples(distance_method, distance_margin, custom_codes)