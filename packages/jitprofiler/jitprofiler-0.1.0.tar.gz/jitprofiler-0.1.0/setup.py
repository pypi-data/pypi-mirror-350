from setuptools import setup, find_packages

setup(
    name="jitprofiler",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for generating automated data profiling reports.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "plotly",
        "scipy",
    ],
    python_requires=">=3.6",
)
