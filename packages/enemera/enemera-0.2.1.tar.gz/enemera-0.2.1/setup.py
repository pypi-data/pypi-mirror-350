from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enemera",
    version="0.2.0",
    author="Francesco Casamassima",
    author_email="dev@elnc.eu",
    description="API client for Enemera energy data API with enhanced functionality and enums",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fracasamax/enemera-api-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
        "pandas>=1.0.0",
        "pytz>=2023.3",
        "pandas>=1.0.0",
        "pytz>=2023.3"
    ],
    extras_require={
        "polars": ["polars>=0.7.0"],
        "excel": ["openpyxl>=3.0.0"],
        "excel-xlsxwriter": ["xlsxwriter>=3.0.0"],
        "all": ["polars>=0.7.0", "openpyxl>=3.0.0", "xlsxwriter>=3.0.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "isort>=5.12.0", "flake8>=6.0.0"],
    }
)
