from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="clipclean",
    version="1.0.0",
    author="Kevin O'Connor",
    description="A simple GUI tool for cleaning text copied from LLM outputs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinobytes/clipclean",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "clipclean=clipclean.gui:main",
        ],
    },
    keywords="text cleaning, llm, ai, clipboard, gui",
    project_urls={
        "Bug Reports": "https://github.com/kevinobytes/clipclean/issues",
        "Source": "https://github.com/kevinobytes/clipclean",
    },
)