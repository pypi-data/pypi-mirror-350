

import os

def dimRed():
    _read_file('dimRed.txt')

def model2_read():
    _read_file('model2.txt')

def model3_read():
    _read_file('model3.txt')

def _read_file(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    try:
        with open(file_path, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"{filename} not found.")
