from setuptools import setup, find_packages

setup(
    name="impkinpy",
    version="0.1.0",
    author="Vitek",
    author_email="your.email@example.com",
    description="Library for mechanics and astronomy",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Viktor640266/impkinpy",  # если есть репозиторий
    packages=find_packages(),
        install_requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # или другая лицензия
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)