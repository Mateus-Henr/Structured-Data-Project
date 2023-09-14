from setuptools import setup, find_packages

setup(
    name='bank_project',
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    description='Description of your package',
    packages=find_packages(),
    install_requires=[
        'peewee',
        'psycopg2-binary',
        'mercadopago',
        'pillow',
        'fpdf',
        'requests',
        'flask'
    ],
)