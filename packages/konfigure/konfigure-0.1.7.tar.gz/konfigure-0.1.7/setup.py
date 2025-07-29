from setuptools import setup, find_packages

setup(
    name="konfigure",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "jinja2>=3.0.0",
    ],
    author="Konfigure Team",
    author_email="example@example.com",
    description="A YAML-based configuration management tool for separating code from prompts in LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunnybak/konfigure",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
