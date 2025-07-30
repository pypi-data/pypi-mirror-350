from setuptools import setup, find_packages

setup(
    name="wordle-cli",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pyfiglet"],
    entry_points={
        "console_scripts": [
            "wordle=wordle.game:main",
        ],
    },
)
