from setuptools import setup, find_packages

VERSION = "1.0.1"
SHORT_DESCRIPTION = "Twitter X-Client-Transaction-Id generator written in python."

# with open("requirements.txt") as file:
#     dependencies = file.read().splitlines()
with open("README.md", "r", encoding="utf-8") as file:
    DESCRIPTION = file.read()

setup(
    name="linkgrid-x-transaction-id",
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Deep Saha",
    author_email="hiremeasadeveloper@gmail.com",
    license="MIT",
    url="https://github.com/OfficialDeepSaha/Transaction-ID-Generator",
    packages=find_packages(),
    keywords=[
        "x-transaction-id",
        "twitter transaction id",
        "client transaction id twitter",
        "tid generator",
        "x client transaction id generator",
        "xid twitter",
        "twitter api"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    'beautifulsoup4>=4.9.3',
    'requests>=2.25.1',
    'aiohttp>=3.8.0',
],
    python_requires=">=3.7"
)

