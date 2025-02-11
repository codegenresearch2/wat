__version__ = "0.1.2"  # should be in sync with pyproject.toml

from setuptools import setup

if __name__ == "__main__":
    setup(
        name="your_package_name",
        version=__version__,
        packages=["your_package_name"],
        install_requires=[
            # List your dependencies here
        ],
        # Additional setup parameters can be added here
    )