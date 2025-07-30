from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='rvgarci-cursofiap-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='Rafael Garcia',
    author_email='rvgarci@gmail.com',
    url='https://github.com/rvgarci/cursofiap.git',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
