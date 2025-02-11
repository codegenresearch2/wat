__version__ = "0.1.2"  # should be in sync with pyproject.toml

from setuptools import setup

setup(
    name="your_package_name",
    version=__version__,
    packages=["your_package_name"],
    install_requires=[
        # List your dependencies here
    ],
    author="Your Name",
    description="A brief description of your package",
    url="https://github.com/yourusername/yourpackagename",
    # Additional setup parameters can be added here
)