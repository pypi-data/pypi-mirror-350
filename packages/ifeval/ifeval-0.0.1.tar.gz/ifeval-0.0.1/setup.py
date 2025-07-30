from setuptools import setup, find_packages

setup(
    name="ifeval",
    version="0.0.1",
    description="Evaluate all if-statement predicates in a Python file",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikolai Krivoshchapov",
    url="https://gitlab.com/knvvv/ifeval",
    packages=find_packages(include=["ifeval", "ifeval.*"]),
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "ifeval=ifeval.__main__:main",
        ],
    },
    install_requires=[
        "libcst",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
