from setuptools import setup, find_packages

setup(
    name='datum_authorization',
    version='0.1.4',
    description='A description of your module',
    author='DatumDev',
    author_email='DatumDev@example.com',
    packages=find_packages(),
    install_requires=[
        'jose','PyJWT'
    ],
    python_requires='>=3.11',
)
