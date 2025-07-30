from setuptools import setup, find_packages

# Lendo o README.md para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

_VERSION = "2.0" 

setup(
    name="duanbima",
    version=_VERSION,
    author="Lucas Soares",
    author_email="lcs-soares@hotmail.com",
    description="Biblioteca Python para manipulação de datas úteis com base no calendário ANBIMA.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(), 
    python_requires='>=3.7', 

    package_data={
        'duanbima': ['anbima_holidays.txt'], 
    },

)