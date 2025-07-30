import json
import os

# Example dictionary data
data = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "is_student": False
}


def write_data(data: dict, filepath: os.path):
    try:
        with open(str(filepath), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print (e)
        return 1
    return 0


def read_data(filepath: os.path):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
    except Exception as e:
        print (e)
        return 1
    return loaded_data