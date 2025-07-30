from setuptools import setup, find_packages

setup(
    name="equation_matrix",
    version="0.1.0",
    author="Debkumar Singha Roy,Sunita Agarwala,Kamal Agarwala",
    author_email="debkumar.singha8@gmail.com",
    description="A robust and user-friendly Python package for executing diverse mathematical operations with high precision and efficiency.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "equation_matrix=equation_matrix.calculator:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)