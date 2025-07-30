from setuptools import setup, find_packages

setup(
    name='gyatModel2',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'gyat_model': ['dimRed.txt', 'model2.txt', 'model3.txt'],
    },
    author='Micheal Scofield',
    description='A sample package that prints text file content',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
