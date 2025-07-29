from setuptools import setup, find_packages

setup(
    name="Openix",
    version="1.0.0",
    description="A simple  chess openings (ECO) library for Python.",
    author="0xh7",
    author_email="fjdjfjd1424@gmail.com",
    packages=find_packages(),
    install_requires=[
        "python-chess",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    url="https://github.com/0xh7/Openix-Library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
