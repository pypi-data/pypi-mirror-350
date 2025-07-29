from setuptools import setup, find_packages
from pathlib import Path

# Read README.md in UTF-8 encoding
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="diskcachedb",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'diskcachedb': ['templates/*.html'],
    },
    install_requires=[
        "diskcache>=5.6.1",
        "bson>=0.5.10",
        "flask>=2.0.0"
    ],
    author="Anandan B S",
    author_email="anandanklnce@gmail.com",
    description="A MongoDB-like query interface using diskcache for persistent storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anandanklnce/diskcache-db",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="database, cache, mongodb, diskcache, persistent storage, query"
)
