from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evolvishub-sqlite-adapter",
    version="0.1.0",
    author="Alban Maxhuni, PhD",
    author_email="amaxhuni@evolvis.ai",
    description="A professional async SQLite adapter library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evolvisai/evolvishub-sqlite-adapter",
    project_urls={
        "Homepage": "https://evolvis.ai",
        "Documentation": "https://evolvishub-sqlite-adapter.readthedocs.io/",
        "Repository": "https://github.com/evolvisai/evolvishub-sqlite-adapter.git",
        "Issues": "https://github.com/evolvisai/evolvishub-sqlite-adapter/issues",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
        "Typing :: Typed",
    ],
    python_requires=">=3.9",
    install_requires=[
        "aiosqlite>=0.19.0",
        "typing-extensions>=4.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.1.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
            "build>=1.0.0",
            "wheel>=0.42.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "sphinx-autodoc-typehints>=1.24.0",
        ],
    },
    keywords=["sqlite", "async", "database", "adapter"],
)

if __name__ == "__main__":
    setup() 