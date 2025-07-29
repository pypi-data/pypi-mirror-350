from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evolvishub-db-migration",
    version="0.1.1",
    author="Alban Maxhuni, PhD",
    author_email="a.maxhuni@evolvis.ai",
    description="A professional database migration tool supporting multiple databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evolvisai/evolvishub-db-migration",
    project_urls={
        "Bug Tracker": "https://github.com/evolvisai/evolvishub-db-migration/issues",
        "Documentation": "https://evolvishub-db-migration.readthedocs.io",
        "Source": "https://github.com/evolvisai/evolvishub-db-migration"
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "SQLAlchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "mysql-connector-python>=8.0.0",
        "pyodbc>=4.0.0",
        "alembic>=1.12.1",
        "sqlparse==0.5.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1"
    ],
    extras_require={
        "testing": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0"
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.22.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "db-migrate=db_migration_tool.cli:main"
        ]
    },
    license="MIT"
)
