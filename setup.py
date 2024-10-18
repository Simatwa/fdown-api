from setuptools import setup

from setuptools import find_packages

INSTALL_REQUIRE = [
    "cloudscraper==1.2.71",
    "bs4==0.0.1",
]

cli_reqs = [
    "tqdm==4.66.3",
    "colorama==0.4.6",
]

EXTRA_REQUIRE = {"cli": cli_reqs}

setup(
    name="fdown-api",
    version="0.0.2",
    license="GPLv3",
    author="Smartwa",
    maintainer="Smartwa",
    author_email="simatwacaleb@proton.me",
    description="Unofficial Python wrapper for fdown.net",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/Simatwa/fdown-api",
    project_urls={
        "Bug Report": "https://github.com/Simatwa/fdown-api/issues/new",
        "Homepage": "https://github.com/Simatwa/fdown-api",
        "Source Code": "https://github.com/Simatwa/fdown-api",
        "Issue Tracker": "https://github.com/Simatwa/fdown-api/issues",
        "Download": "https://github.com/Simatwa/fdown-api/releases",
        "Documentation": "https://github.com/Simatwa/fdown-api/",
    },
    entry_points={
        "console_scripts": [
            "fdown = fdown_api.console:main",
        ],
    },
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    python_requires=">=3.10",
    keywords=[
        "facebook",
        "fdown",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Free For Home Use",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
