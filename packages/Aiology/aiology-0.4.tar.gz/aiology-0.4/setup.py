from setuptools import setup , find_packages 

with open("README.md","r") as file:
    readme = file.read()

setup(
    name="Aiology",
    version="0.4",
    author="Seyed Moied Seyedi (Single Star)",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown"
)