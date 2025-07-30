import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fin:
    REQS = fin.read().splitlines()

with open("requirements-dev.txt", "r") as fin:
    REQS_DEV = [item for item in fin.read().splitlines() if not item.endswith(".txt")]

JINJA_EXTRA = [item.split(" #", 1)[0] for item in REQS_DEV if "# extras_require jinia" in item]
TOMLI_EXTRA = [item.split(" #", 1)[0] for item in REQS_DEV if "# extras_require tomli" in item]

setuptools.setup(
    name="sag-py-logging",
    version="0.4.2",
    description="Initialize logging from a configuration json",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/SamhammerAG/sag_py_logging",
    author="Samhammer AG",
    author_email="support@samhammer.de",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
    ],
    keywords="logging, extra, fields",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"sag_py_logging": ["py.typed"]},
    python_requires=">=3.12",
    install_requires=REQS,
    extras_require={"dev": REQS_DEV, "jinja": JINJA_EXTRA, "toml": TOMLI_EXTRA},
    project_urls={
        "Documentation": "https://github.com/SamhammerAG/sag_py_logging",
        "Bug Reports": "https://github.com/SamhammerAG/sag_py_logging/issues",
        "Source": "https://github.com/SamhammerAG/sag_py_logging",
    },
)
