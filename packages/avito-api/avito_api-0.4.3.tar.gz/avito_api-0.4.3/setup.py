from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="avito-api",
    version="0.4.3",
    author="Aleksandr Gnatenko",
    author_email="alexgnat@gmail.com",
    description="Библиотека для работы с API Авито",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.talisman.ms/alekskdr/avito-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.23.0",
        "pydantic>=2.6,<3.0",
    ],
    extras_require={
        "log": ["loguru>=0.6.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.950",
            "flake8>=4.0.0",
        ],
    },
)
