from setuptools import setup, find_packages

setup(
    name="statscata",
    version="0.1.0",
    description="A custom Python project for suricata performance analysis.",
    author="Colin Evrard",
    author_email="colin.evrard@uclouvain.be",
    url="https://github.com/supercoolin/statscata",  # If you have a repository
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g.,
        'pandas>=2.2.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
