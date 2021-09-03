from setuptools import setup, find_packages

install_requires=[
    'pandas',
    'rdflib',
    'pyrml @ git+ssh://git@github.com/anuzzolese/pyrml.git'
]

setup(name='KE_Soil_Heritage', version='0.1.0', packages=find_packages(),
      install_requires=install_requires)
