from setuptools import setup, find_packages

setup(
    name = "BinaryFileReader",
    version = "3.0.4",

    packages = ["BinaryFileReader"],
    install_requires = ["PytonToolsKit==1.2.4", "PegParser>=1.1.4", "RC4Encryption==0.0.2", "RC6Encryption==1.0.1"],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
    maintainer = "Maurice Lambert",
    maintainer_email = "mauricelambert434@gmail.com",
 
    description = "This package reads binary file to exports strings or prints content as hexadecimal.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/BinaryFileReader',
    download_url="https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.pyz",
    project_urls={
        "Github": "https://github.com/mauricelambert/BinaryFileReader",
        "Strings Documentation": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.html",
        "Strings Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.pyz",
        "Strings Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.exe",
        "HexaReader Documentation": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.html",
        "HexaReader Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.pyz",
        "HexaReader Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.exe",
        "MagicStrings Documentation": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/MagicStrings.html",
        "MagicStrings Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/MagicStrings.pyz",
        "MagicStrings Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/MagicStrings.exe",
        "Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.pyz",
        "Python Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.exe",
    },
 
    classifiers = [
        "Topic :: Security",
        "Environment :: Console",
        "Topic :: System :: Shells",
        "Operating System :: MacOS",
        'Operating System :: POSIX',
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: System :: System Shells",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows",
        "Topic :: System :: Systems Administration",
        "Intended Audience :: System Administrators",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],

    keywords=['strings', 'hexadecimal', 'hexadecimal-reader', 'binary-file', 'reverse', 'binary-reader', 'binary-viewer'],
 
    scripts = [],
    entry_points = {
        'console_scripts': [
            'Strings = BinaryFileReader:strings',
            'MagicStrings = BinaryFileReader:magic',
            'HexaReader = BinaryFileReader:hexaread',
            'BinaryFileReader = BinaryFileReader.__main__:main',
        ],
    },

    platforms=['Windows', 'Linux', "MacOS"],
    license="GPL-3.0 License",
    python_requires='>=3.8',
)