from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kbki-classifier-deplearning-s", 
    version="0.1.3",
    author="deplearning",
    author_email="devinasawitrii@gmail.com",  
    description="KBKI (Klasifikasi Baku Komoditi Indonesia) Text Classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deplearning-s/kbki-classifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "h2o>=3.40.0",
        "gradio>=3.0.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "gdown>=4.0.0",
        "openpyxl>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "kbki-classifier=kbki_classifier.app:main",
        ],
    },
)
