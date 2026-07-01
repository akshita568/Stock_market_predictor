from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function reads and processes requirements.txt to return a list of
    dependencies, intentionally stripping out editable installation markers like '-e .'.
    """
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and the editable package installation flag
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("Warning: requirements.txt file not found during setup processing.")

    return requirement_lst

setup(
    name="stock_predictor",
    version="0.0.1",
    author="Akshita",
    author_email="sakshita229@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)