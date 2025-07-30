from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the contents of requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="evolvishub-ollama-adapter",
    version="0.1.0",
    author="Alban Maxhuni",
    author_email="a.maxhuni@evolvis.ai",
    description="A professional Python adapter for Ollama, providing a clean and type-safe interface for interacting with Ollama models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evolvis/evolvishub-ollama-adapter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "evolvishub_ollama_adapter": ["assets/png/*.png"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "yaml": ["PyYAML>=6.0"],
    },
    project_urls={
        "Documentation": "https://evolvis.ai/docs/evolvishub-ollama-adapter",
        "Source": "https://github.com/evolvis/evolvishub-ollama-adapter",
        "Tracker": "https://github.com/evolvis/evolvishub-ollama-adapter/issues",
    },
) 