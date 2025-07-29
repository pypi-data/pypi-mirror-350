from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mlflow-advanced",
    version="1.0.0",
    author="Jatin Hans",
    author_email="jatin.hans@example.com",
    description="A high-performance machine learning library with advanced algorithms and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jatiiiiiinnnnnn/mlflow-advanced",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.0.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "joblib>=1.0.0",
        "tqdm>=4.62.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8", "mypy"],
        "docs": ["sphinx", "sphinx-rtd-theme"],
    },
    license="MIT",
    keywords="machine learning mlflow neural networks optimization interpretability",
)
