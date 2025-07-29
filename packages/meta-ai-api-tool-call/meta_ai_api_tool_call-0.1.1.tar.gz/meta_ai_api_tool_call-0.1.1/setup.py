from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="meta_ai_api_tool_call",
    version="0.1.1",
    description="A Python package for interacting with Meta AI API (reverse engineered) with tool calls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Meet Gor",
    author_email="gormeet711@gmail.com",
    url="https://github.com/mr-destructive/meta_ai_api_tool_call",
    packages=find_packages(),
    install_requires=[
        "requests-html",
        "beautifulsoup4",
        "requests",
        "lxml",
        "lxml_html_clean"
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
