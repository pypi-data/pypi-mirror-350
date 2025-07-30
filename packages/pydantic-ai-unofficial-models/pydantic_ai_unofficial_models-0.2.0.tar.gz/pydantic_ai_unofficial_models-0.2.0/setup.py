from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydantic_ai_unofficial_models",
    version="0.2.0",
    description="A collection of unofficial models for pydantic-ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Meet Gor",
    author_email="gormeet711@gmail.com",
    url="https://github.com/mr-destructive/pydantic-ai-unofficial-models",
    packages=find_packages(),
    install_requires=[
        "pydantic-ai",
        "meta-ai-api-tool-call",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Source": "https://github.com/mr-destructive/meta_ai_api_tool_call",
        "Tracker": "https://github.com/mr-destructive/meta_ai_api_tool_call/issues",
    },
    include_package_data=True,
)
