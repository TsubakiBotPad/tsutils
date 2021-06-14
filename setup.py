import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsutils",
    version="3.4.1",
    author="The Tsubotki Team",
    author_email="69992611+TsubakiBotPad@users.noreply.github.com",
    license="MIT",
    description="A collection of helper commands for Red-DiscordBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TsubakiBotPad/tsutils",
    packages=setuptools.find_packages(),
    install_requires=["pytz", "aiohttp", "backoff", "discord-menu"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
