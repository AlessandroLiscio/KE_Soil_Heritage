from setuptools import setup, find_packages

install_requires=[
    'pandas',
    'rdflib'
]

setup(name='KE_Soil_Heritage', version='1.0.0', packages=find_packages(),
      install_requires=install_requires, dependency_links=['https://github.com/anuzzolese/pyrml/tarball/master'])
