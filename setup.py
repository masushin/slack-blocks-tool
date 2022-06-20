import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setuptools.setup(
    name="slackblockstool", # Replace with your own username
    version="0.2.4",
    author="shinsuke masuda",
    author_email="shinsuke.masuda@gmail.com",
    description="Tool for Slack Blocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=_requires_from_file('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
