from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="contacted",
    version="1.0.0",
    author="Your Name",
    author_email="lawrence@contacted.io",
    description="Official Contacted Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LawrenceGB/contacted-python",
    project_urls={
        "Bug Tracker": "https://github.com/LawrenceGB/contacted-python/issues",
        "Documentation": "https://contacted.gitbook.io",
        "Homepage": "https://contacted.io",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Communications :: Email",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="contacted ai api sdk email automation",
    include_package_data=True,
    zip_safe=False,
)