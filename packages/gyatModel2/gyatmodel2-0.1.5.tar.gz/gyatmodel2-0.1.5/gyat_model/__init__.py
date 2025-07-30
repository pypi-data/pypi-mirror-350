import os

def adaline():
    _read_file('adaline.txt')

def boosting():
    _read_file('boosting.txt')

def dimRed():
    _read_file('dimRed.txt')

def elbowKmeans():
    _read_file('elbowKmeans.txt')

def intro():
    _read_file('intro.txt')

def logReg():
    _read_file('logReg.txt')

def perceptron():
    _read_file('perceptron.txt')

def perceptronGreDes():
    _read_file('perceptronGreDes.txt')

def prolog8():
    _read_file('prolog8.txt')

def prologTic():
    _read_file('prologTic.txt')

def prologWater():
    _read_file('prologWater.txt')

def randomForest():
    _read_file('randomForest.txt')

def svm():
    _read_file('svm.txt')


def all():
    """
    Print all available model file names listed in all.txt
    """
    _read_file('all.txt')

def _read_file(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Safely print even if terminal can't handle certain unicode characters
            text = f.read()
            sys.stdout.buffer.write(text.encode('utf-8'))
    except FileNotFoundError:
        print(f"{filename} not found.")
