from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
setup(
  name="pysyscontrol",
  version="2.0.0",
  author="Shagedoorn1",
  author_email="svenhagedoorn@gmail.com",
  description="A Python package for Control Systems Analysis",
  license_files=["LICENSE"],
  include_package_data=True,
  long_description=(this_dir/ "README.md").read_text(encoding="utf-8") + "\n\n" + (this_dir / "CHANGELOG.md").read_text(encoding="utf-8"),
  url="https://github.com/Shagedoorn1/PySysControl",
  long_description_content_type="text/markdown",
  packages=find_packages(),
  install_requires= [
    "numpy>=1.26",
    "matplotlib>=3.7",
    "sympy>=1.12",
    "scipy>=1.11",
    ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.12"
)