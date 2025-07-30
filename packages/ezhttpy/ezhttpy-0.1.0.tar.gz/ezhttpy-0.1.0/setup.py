from setuptools import setup, find_packages

setup(
    name='ezhttpy',
    version='0.1.0',
    description='Jednoduchý HTTP server s vlastnými príkazmi a HTML podporou',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Denis Varga',
      url='https://easy_http.denisvarga.eu/',
    author_email='mail@denisvarga.eu',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
