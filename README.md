# KE_Soil_Heritage
Analysing indicators of soil consumption in Italy in order to understand and constructing a knowledge graph.
 
This projects provides the following facilities for enhancing user experience: 
 - Virtuoso as SPARQL enpoint;
 - LODE for visualising ontologies as HTML;
 - WebVOWL for visualising ontologies with the Visual Notation for OWL Ontologies (VOWL);
 - LodView for browsing ontology entities as well as controlloed vocabularies entities.

### Virtual Environmment
It is suggested that developers interested in editing the project, do it in a safe virtual environment.

Initializing a new python environment can be done in the following way:

```
$> python -m venv c:\path\to\myenv
```
Activating the python environment can be done in the following way:

```
$> source c:\path\to\myenv\bin\activate
```

An example of a possible python virtual environment for this project could be:

```
$> python -m kenv usr/bin/kenv 
```

To activate the environment:

```
$> source /usr/bin/kenv/bin/activate
```


### Installation
KE_Soil_Heritage requires Python 3.
Once the source code has been downladed it is possible to install the Python package by means of pip. For example:

```
pip install .
```

### Build and run
The project relies on Docker.
To build the containers type the following command in the terminal having the root of the project as base folder:
```
$> docker-compose build
```
To run the containers type the following command in the terminal having the root of the project as base folder:
```
$> docker-compose up
```

### Usage
Once the containers are up and assuming that `localhost` is the reference host, users can access:
 - the SPARQL endpoint at http://localhost:8890/sparql;
 - LODE at http://localhost:9090/lode;
 - WebVOWL at http://localhost:8080/webvowl
 - LodView at http://localhost:8080/lodview.

