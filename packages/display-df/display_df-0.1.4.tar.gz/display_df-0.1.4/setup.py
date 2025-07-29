from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="display_df",
    version="0.1.4",
    description="Interactive DataFrame viewer with enhanced search (PyQt5)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=["pandas", "PyQt5"],
    python_requires=">=3.7",
    url="https://github.com/yourusername/display_df",  # Update this if you publish to GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
