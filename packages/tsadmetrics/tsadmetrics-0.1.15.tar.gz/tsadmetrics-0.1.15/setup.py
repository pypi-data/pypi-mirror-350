from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tsadmetrics",
    version="0.1.15",
    author="Pedro Rafael Velasco Priego",
    author_email="i12veprp@uco.es",
    description="A library for time series anomaly detection metrics and evaluation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pathsko/TSADmetrics",
    packages=find_packages(where='tsadmetrics'),  # Cambiado para que busque dentro de la carpeta tsadmetrics
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "joblib==1.4.2",
        "numpy==1.24.4",
        "pandas==2.0.3",
        "PATE==0.1.1",
        "patsy==0.5.6",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "scikit-learn==1.3.2",
        "scipy==1.10.1",
        "six==1.16.0",
        "statsmodels==0.14.1",
        "threadpoolctl==3.5.0",
        "tzdata==2024.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "ipython>=7.0",
            "sphinx",
            "sphinx-rtd-theme",
            "numpydoc",
            "myst-parser",
        ],
    },
)
