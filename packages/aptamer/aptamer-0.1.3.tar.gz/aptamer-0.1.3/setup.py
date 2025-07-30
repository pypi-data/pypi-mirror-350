from setuptools import setup, find_packages

setup(
    name='aptamer',
    version='0.1.3',
    description='Evolve DNA aptamers using RNA folding energy',
    packages=find_packages(),
    install_requires=[
        'viennarna',
        'pytest',
    ]
)
