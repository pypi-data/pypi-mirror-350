from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eizen-sdk",
    version="0.1.11",
    packages=find_packages(),
    install_requires=["PyJWT>=2.10.1", "requests>=2.31.0", "urllib3>=2.0.7", "pyyaml>=6.0.2"],
    author="Pardhu",
    description="A SDK to consume Eizen services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    keywords="eizen sdk",
)
