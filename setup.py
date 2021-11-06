import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsutils",
    version="5.3.0",
    author="The Tsubotki Team",
    author_email="69992611+TsubakiBotPad@users.noreply.github.com",
    license="MIT",
    description="A collection of helper commands for Red-DiscordBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TsubakiBotPad/tsutils",
    packages=setuptools.find_packages(),
    install_requires=[
        "aiohttp>=3.7.4",
        "backoff>=1.10.0",
        "discord.py>=1.7.3",
        "discord_menu>=0.16.13",
        "pytz>=2021.1",
        "Red-DiscordBot>=3.4.14",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
