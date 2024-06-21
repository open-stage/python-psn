from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypsn",
    version="0.2.1",
    long_description=long_description,
    description="PosiStageNet parser",
    license="MIT",
    url="https://github.com/open-stage/python-psn",
    long_description_content_type="text/markdown",
    author="vanous",
    author_email="noreply@nodomain.com",
    packages=["pypsn"],
    project_urls={
        "Source": "https://github.com/open-stage/python-psn",
        "Changelog": "https://github.com/open-stage/python-psn/blob/master/CHANGELOG.md",
    },
)
