from setuptools import setup

setup(
    name="tube-search",
    version="0.0.2.1",
    license="MIT License",
    author="BubbalooTeam",
    author_email="bubbalooteam@proton.me",
    keywords=["tube search", "tube_search"],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    description="🔎 Search for videos, channels and playlists on YouTube quickly and easily.",
    packages=["tube_search"],
    install_requires=[
        "httpx[http2]",
    ],
)