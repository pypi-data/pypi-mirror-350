from setuptools import setup, find_packages

setup(
    name="wnote",
    version="0.5.2",
    description="Terminal Note Taking Application with beautiful UI",
    author="imnahn",
    py_modules=["wnote", "__init__"],
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "requests>=2.28.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "markdown>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wnote=wnote:cli",
        ],
    },
    python_requires=">=3.7",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
) 