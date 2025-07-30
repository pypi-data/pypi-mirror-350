from setuptools import setup, find_packages

setup(
    name='mondip',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scikit-learn',
    ],
)