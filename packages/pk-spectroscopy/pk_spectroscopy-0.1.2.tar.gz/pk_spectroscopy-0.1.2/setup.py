from pathlib import Path
from setuptools import setup, find_packages

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

version_ns = {}
exec((ROOT / "src/pk_spectroscopy/_version.py").read_text(), version_ns)

setup(
    name="pk_spectroscopy",
    version=version_ns["__version__"],
    description="Advanced analysis of objects with complex acid composition",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mikhail Markovskii",
    author_email="m.markovsky@gmail.com",
    url="https://github.com/Sciencealone/pk_spectroscopy",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy==2.2.6",
        "scipy==1.15.3",
        "pandas==2.2.3",
        "streamlit==1.45.1",
        "plotly==6.1.1",
        "plotly-express==0.4.1",
    ],
    extras_require={
        "dev": ["pytest", "black", "ruff", "mypy", "coverage"],
    },
    entry_points={
        "console_scripts": [
            "pk_spectroscopy = pk_spectroscopy.app.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
    include_package_data=True,
    zip_safe=False,
)