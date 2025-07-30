from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="delimux",
    use_scm_version=True,
    setup_requires=["setuptools-scm"],
    description="API for the delimux device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian Huber",
    author_email="huberse@phys.ethz.ch",
    url="https://gitlab.phys.ethz.ch/cmtqo-projects/delicate/delimux",
    packages=find_packages(include=["delimux", "delimux.*"]),
    python_requires=">=3.8",
)