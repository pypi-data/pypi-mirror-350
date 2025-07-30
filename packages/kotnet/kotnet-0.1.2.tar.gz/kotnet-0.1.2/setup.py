from setuptools import setup, find_packages

setup(
    name="kotnet",
    version="0.1.2",
    description="Console text formatting and animations library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="EnderDragon",
    author_email="rhdhf909@gmail.com",
    packages=find_packages(),
    packges=["kotnet"],
    include_package_data=True,  
    install_requires=[
        'colorama >= 0.4.4',
        'tqdm >= 4.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)