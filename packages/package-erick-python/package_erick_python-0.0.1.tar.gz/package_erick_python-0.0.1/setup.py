from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name='package_erick_python',
    version='0.0.1',
    author='Erick Santos',
    author_email='santos.erisk@gmail.com',
    description='Aprendendo a utilizar packages em Python',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Erisksnt/image-processing-package',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Ajuste conforme sua licença
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)