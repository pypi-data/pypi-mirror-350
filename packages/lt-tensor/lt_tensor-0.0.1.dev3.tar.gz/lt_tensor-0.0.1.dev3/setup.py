from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version="0.0.1dev3",
    name="lt-tensor",
    description="General utilities for PyTorch and others. Built for general use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gr1336/lt-tensor/",
    install_requires=[
        "torch>=2.2.0",
        "torchaudio>=2.2.0",
        "numpy>=1.26.4",
        "tokenizers",
        "pyyaml>=6.0.0",
        "numba>0.60.0",
        "lt-utils==0.0.1.dev0",
    ],
    author="gr1336",
    license="Apache Software License (Apache-2.0)",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
    ],
)
