from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kotnet",
    version="0.1.0",
    author="EnderDragon",
    author_email="rhdhf909@gmail.com",
    description="Библиотека для стилизации консольных приложений",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enderdragon-lts/",
    packages=find_packages(),
    install_requires=["colorama >= 0.4.4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)