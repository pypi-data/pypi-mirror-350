from setuptools import setup, find_packages

setup(
    name='gyatModel2',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'gyat_model': [
            'adaline.txt',
            'boosting.txt',
            'dimRed.txt',
            'elbowKmeans.txt',
            'intro.txt',
            'logReg.txt',
            'perceptron.txt',
            'perceptronGreDes.txt',
            'prolog8.txt',
            'prologTic.txt',
            'prologWater.txt',
            'randomForest.txt',
            'svm.txt',
            'model2.txt',
            'model3.txt',
            'all.txt'
        ],
    },
    author='Micheal Scofield',
    description='A sample package that prints content of AI/ML model text files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
