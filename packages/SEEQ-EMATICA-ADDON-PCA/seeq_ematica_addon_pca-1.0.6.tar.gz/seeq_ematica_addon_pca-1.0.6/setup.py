from setuptools import setup, find_packages

# Read long description from the README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from the requirements.txt file
with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.read().splitlines()

setup(
    name="SEEQ_EMATICA_ADDON_PCA",
    version="1.0.6",  # Current version
    author="Alessandro Robbiano",
    author_email="alessandro.robbiano@e-matica.it",
    description="PCA Package for Seeq Addons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
)
