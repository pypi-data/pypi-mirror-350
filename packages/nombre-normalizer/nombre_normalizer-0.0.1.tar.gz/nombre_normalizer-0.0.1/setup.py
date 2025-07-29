"""
Setup script para el paquete nombre-normalizer.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nombre-normalizer",
    version="0.0.1",
    author="Mon Maldonado",
    author_email="pigmonchu@gmail.com",
    description="Normalizador de nombres y apellidos en español",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/nombre-normalizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "nombre-normalizer=nombre_normalizer.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nombre_normalizer": ["data/*.txt", "data/*.json"],
    },
)