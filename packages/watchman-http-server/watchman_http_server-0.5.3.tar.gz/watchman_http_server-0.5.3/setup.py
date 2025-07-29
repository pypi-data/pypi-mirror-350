# Setup script for packaging
from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.readlines()
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.startswith("#")
    ]


setup(
    name="watchman_http_server",
    version="0.5.3",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "watchman-http-server=watchman_http_server.commands:cli",
        ],
    },
    author="Watchman",
    author_email="support@watchman.bj",
    description="Un serveur HTTP FastAPI pour récupérer les applications installées",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
