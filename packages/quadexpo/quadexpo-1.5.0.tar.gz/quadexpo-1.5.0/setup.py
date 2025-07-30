from setuptools import setup, find_packages

setup(
    name="quadexpo",
    version="1.5.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A mathematical library implementing the Quadexpo function.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quadexpo",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
