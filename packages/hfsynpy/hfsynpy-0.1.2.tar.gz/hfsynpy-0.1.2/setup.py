from setuptools import setup, find_packages

setup(
    name="hfsynpy",
    version="0.1.2",
    description="A Python library for synthesis and analysis of high frequency component (currently only microstrip transmission lines), providing accurate models and convenient tools for PCB and RF design.",
    author="Dominik Mair",
    author_email="dominik.mair@uibk.ac.at",
    url="https://github.com/GenerativeAntennaDesign/hfsynpy",
    project_urls={
        "Documentation": "https://generativeantennadesign.github.io/hfsynpy/",
        "Source": "https://github.com/GenerativeAntennaDesign/hfsynpy",
    },
    packages=find_packages(where="."),
    install_requires=[
        # No external dependencies required
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="GPL-2.0-or-later",
    keywords="microstrip synthesis analysis PCB RF design high frequency transmission line",
)
