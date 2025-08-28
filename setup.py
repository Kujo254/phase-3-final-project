from setuptools import setup, find_packages

setup(
    name="library_management",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "SQLAlchemy"
    ],
    entry_points={
        "console_scripts": [
            "library-cli=library_management.cli:cli",
        ],
    },
)
