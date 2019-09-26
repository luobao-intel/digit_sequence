
from setuptools import setup, find_packages

setup(
    name="create_digit_sequence",
    version="1.0",
    description="A package tool for training data augmentation of OCR model",
    url="https://github.com/luobao-intel/digit_sequence",
    author="Zou Luobao",
    author_email="leiling@sjtu.edu.cn",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'Pillow',
        'opencv-python',
        'numpy',
        'six',
        'matplotlib'
    ],
    scripts=[],
)