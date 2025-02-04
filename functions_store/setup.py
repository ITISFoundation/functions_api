from setuptools import setup, find_packages

setup(
    name="functions_store",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.23",
        "pydantic>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "functions-store=functions_store.main:app",
        ],
    },
)

