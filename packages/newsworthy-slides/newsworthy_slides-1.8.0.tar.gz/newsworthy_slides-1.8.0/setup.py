from setuptools import setup
from version import version, name, authors, email, short_desc


def readme():
    """Import README for use as long_description."""
    with open("README.rst") as f:
        return f.read()


repo = "https://gitlab.com/newsworthy/newsworthy_slides"

setup(
    name=name,
    version=version,
    description=short_desc,
    long_description=readme(),
    long_description_content_type='text/x-rst',
    url=repo,
    author=authors,
    author_email=email,
    license="MIT",
    packages=[name],
    zip_safe=False,
    python_requires='~=3.5',
    install_requires=[
        "python-pptx>=0.6.18",
        "pytest>=3.10.1",
        "beautifulsoup4>=4.7.1",
        "requests>=2.22.0",
    ],
    include_package_data=True,
    download_url="{}/archive/{}.tar.gz".format(repo, version),
)
