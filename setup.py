from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="st_oauth",
    packages=find_packages(),
    version='0.0.1',
    description='Helper tools for connecting to data sources from Streamlit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Brian Hess',
    author_email='brian.hess@snowflake.com',
    license='LICENSE.txt',
    install_requires=['streamlit', 'requests', 'jwt']
)