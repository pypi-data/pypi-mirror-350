import json
import os


# Add new codes to include in the tests
def raw_data():
    new_codes = {}
    new_codes["0"] = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [108, 16, 6]
    }
    return new_codes


def save_raw_data_file(data):
    with open("known_codes", "w") as file:
        file.write("{")
        for i, key in enumerate(data):
            file.write(f"\"{key}\": {str(data[key])}")
            if i < len(data) - 1:
                file.write(",")
        file.write("}")
        file.flush()
        file.close()


def add_raw_data_to_json():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(folder_path, "known_codes")
    with open(file_path, "r") as file:
        old_codes = json.loads(file.read().replace("\'", "\""))
        new_codes = raw_data()

        num_codes = len(old_codes)
        num_codes_to_add = len(new_codes)

        for i in range(num_codes, num_codes + num_codes_to_add):
            if str(i) in old_codes:
                raise ValueError(f"code numbered {i} already exists")
            old_codes[str(i)] = new_codes[str(i - num_codes)]

    save_raw_data_file(old_codes)



if __name__ == "__main__":
    add_raw_data_to_json()
    pass