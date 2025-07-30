from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="desafio-dio-erisksnt",
    version="0.0.1",
    author="Erick Santos",
    author_email="santos.erisk@gmail.com",
    description="Aplicando os conhecimentos obtidos através da aula de criação de packages da DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Erisksnt/simple-package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)
