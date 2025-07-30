from src.core_optimised import BBCodeOptimised
import json
import os

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


def run_bbcode_cached_examples(custom_codes, distance_method, distance_margin):
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
        code = BBCodeOptimised(example["l"], example["m"])

        n, k, d = code.set_expressions(example["a"], example["b"]).generate_bb_code(distance_method = distance_method)
        n_known, k_known, d_known = example["answer"]

        passed = n == n_known and k == k_known and d_known <= d * distance_margin

        if not passed:
            display_code(example, n, k, d)
            exit(1)

        print(f"Code {i} passed.")



if __name__ == "__main__":
    custom_codes = False
    distance_margin = 1.15
    distance_method = 3
    run_bbcode_cached_examples(custom_codes, distance_method, distance_margin)