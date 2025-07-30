from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="medallion-etl",
    version="0.1.0",
    author="Data Engineering Team",
    author_email="info@example.com",
    description="Una librería modular para construir data pipelines con arquitectura medallion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JuanManiglia/medallion-etl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Database",
    ],
    python_requires=">=3.11",
    install_requires=[
        "polars>=1.30",
        "pydantic>=2.7",
        "sqlalchemy>=2.0",
        "prefect>=3.0",
        "requests>=2.25.0",
        "rich>=14.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "medallion-etl=medallion_etl.cli.commands:main",
        ],
    },
    include_package_data=True,
)