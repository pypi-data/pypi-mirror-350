from setuptools import setup, find_packages

setup(
    name="tk_sql_lib",                     # package name
    version="0.1",                         # version number
    packages=find_packages(),              # automatically finds all packages
    include_package_data=True,             # includes files from MANIFEST.in
    install_requires=[                     # dependencies
        # "tkinter" is built-in in Python, so usually no need to specify
        ""                         # optional: use only if needed
    ],
    author="susich",
    description="A simple exam toolkit for GUI and SQLite3 apps using Tkinter.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
