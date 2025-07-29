from setuptools import setup, find_packages
from pathlib import Path


requirements = Path(__file__).parent.joinpath("requirements.txt").read_text().splitlines()


setup(
    name="sports_prediction_framework",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements
)