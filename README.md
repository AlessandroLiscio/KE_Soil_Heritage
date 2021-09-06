# KE_Soil_Heritage
Analysing indicators of soil consumption in Italy in order to understand and constructing a knowledge graph.
 
This projects provides the following facilities for enhancing user experience: 
 - Virtuoso as SPARQL enpoint;
 - LODE for visualising ontologies as HTML;
 - LodView for browsing ontology entities as well as controlloed vocabularies entities.
 - LodLive for visualising ontologies with the effectiveness of data graph representation;

### Build and run
The project relies on Docker. To build and run the containers, navigate to the
root folder of the project and run the following command:
```
docker-compose build && docker-compose up
```

### Usage
Once the containers are up and assuming that `localhost` is the reference host, users can access:
 - the SPARQL endpoint at http://localhost:8890/sparql;
 - LODE at http://localhost:9090/lode;
 - WebVOWL at http://localhost:8080/webvowl
 - LodView at http://localhost:8080/lodview.

## Developers

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
python -m venv usr/bin/.kenv 
```
To activate the environment:
```
source /usr/bin/.kenv/bin/activate
```

### Dependencies Installation
KE_Soil_Heritage requires Python 3.
Once the source code has been downladed it is possible to install its dependencies
by the means of pip using the *requirements.txt* in the *src* folder. For example:
```
pip install -r requirements.txt 
```   
### Data Preparation
Before running the *main.py* file to generate the ontology, the data needs to
be extracted from the *soilc.zip* file and stored in a new *data* folder.

Moreover, some files have weird encoding, and thus need to be converted to UTF-8
for the *main.py* to work properly.

Luckily for you, we prepared a bash file which does exactly that, all you need is
for *unzip* and *iconv* to be installed in your terminal, which is default for most os's.
If this is your case, you just need to navigate to the project *src* folder and run
the following command:
```
chmod +x ./prep_data.sh && ./prep_data.sh
```   
Congrats, now you have your data set up and you are ready to go!

### Create Ontologies Files
All you need to do is to navigate to the project *src* folder and run
the *main.py* script. Once it has finished all the computation, the ontologies
files will be stored in the *src/ontologies* folder.
