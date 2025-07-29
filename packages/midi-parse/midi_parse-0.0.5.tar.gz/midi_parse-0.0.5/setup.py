import setuptools

import midi_parse

setuptools.setup(
    name = "midi_parse",
    version = f"{midi_parse.__version__}",
    description = "A simple MIDI parser written in Python",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    author = "qaqFei",
    author_email = "qaq_fei@163.com",
    url = "https://github.com/qaqFei/midi_parse",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires = [],
    license = "MIT License",
    python_requires = ">=3.12.0"
)
