from setuptools import setup, find_packages

setup(
    name="pkmb",
    version="0.1.2",
    packages=find_packages(),
    description="A comprehensive NLP and Machine Learning package with example implementations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/pkmb",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "nltk>=3.8.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.0.0",
        "requests>=2.25.0",
        "gensim>=4.0.0",
        "scipy==1.11.4",
        "tensorflow>=2.12.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "torch>=2.0.0",
        "PyMuPDF>=1.22.0"
    ],
    package_data={
        'pkmb': ['*.py'],
    },
    include_package_data=True,
    keywords="nlp machine-learning deep-learning text-processing vae lstm word-embeddings",
) 