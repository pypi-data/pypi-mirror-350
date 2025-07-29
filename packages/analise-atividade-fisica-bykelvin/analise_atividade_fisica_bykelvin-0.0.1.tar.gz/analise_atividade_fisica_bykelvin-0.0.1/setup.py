from setuptools import setup, find_packages

setup(
    name='analise-atividade-fisica-bykelvin',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    author='Kelvin',
    description='Pacote para análise de atividades físicas com base em CSV',
)