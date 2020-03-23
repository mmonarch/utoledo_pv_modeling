from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="ut_pv",
    version="0.0.1",
    author="Mark Monarch",
    author_email="mpilmonarch@gmail.com",
    url="https://github.com/mmonarch/utoledo_pv_modeling/",
    packages=find_packages()
)
