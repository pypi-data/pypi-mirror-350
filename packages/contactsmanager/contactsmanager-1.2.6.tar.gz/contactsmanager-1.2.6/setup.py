from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join("contactsmanager", "__init__.py"), "r") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string")

# Read long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="contactsmanager",
    version=version,
    description="Python SDK for ContactsManager API authentication and token generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arpit Agarwal",
    author_email="your-email@example.com",  # Replace with your email
    url="https://github.com/arpwal/contactsmanager-py",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "PyJWT>=2.0.0,<3.0.0",
        "requests>=2.28.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "twine>=4.0.0",
            "build>=0.10.0",
            "httpx>=0.24.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords="api, sdk, contactsmanager, authentication, jwt",
    project_urls={
        "Source": "https://github.com/arpwal/contactmanager",
        "Bug Reports": "https://github.com/arpwal/contactmanager/issues",
    },
)
