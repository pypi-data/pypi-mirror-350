
from setuptools import setup, find_packages

setup(
    name='metawork',
    version='0.1.0',
    description='Biblioteca para manipulação de metadados em arquivos de código, documentos e mídias.',
    author='Seu Nome',
    author_email='seuemail@exemplo.com',
    packages=find_packages(),
    install_requires=[
        'python-docx',
        'openpyxl',
        'Pillow',
        'piexif',
        'mutagen',
        'PyPDF2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
