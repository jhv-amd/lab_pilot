from setuptools import setup, find_packages

setup(
    name="lab-generator",
    version="1.0.0",
    description="AI-powered ML lab kit generator for university courses",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "jinja2>=3.1.0",
        "pyyaml>=6.0",
        "nbformat>=5.7.0",
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "rich>=13.0.0",
        "questionary>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "lab-gen=lab_generator:cli",
        ],
    },
)
