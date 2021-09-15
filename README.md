# KE_Soil_Heritage
Analysing indicators of soil consumption in Italy in order to understand and constructing a knowledge graph.
 
This projects provides the following facilities for enhancing user experience: 
 - Virtuoso as SPARQL enpoint;
 - LODE for visualising ontologies as HTML;
 - LodView for browsing ontology entities as well as controlloed vocabularies entities.
 - LodLive for visualising ontologies with the effectiveness of data graph representation;

### With Docker
The project relies on Docker. To build and run the containers, navigate to the
root folder of the project and run the following command:
```
docker-compose build && docker-compose up
```

### Usage
Once the containers are up and assuming that `localhost` is the reference host, users can access:
 - Virtuoso SPARQL endpoint at http://localhost:8890/sparql
 - LODE at http://localhost/app_en.html
 - LodView at http://localhost:8080/lodview
 - LodLive at http://localhost/app_en.html
 - WebVOWL at http://localhost:8080/webvowl

#### Quick Examples:
Here are some quick links to show how information about the element
"https://soilproject.org/onto/Indicatore" can be visualized using the browser:

 - Virtuoso: http://localhost:8890/sparql?query=select?p?o{%3Chttps://soilproject.org/onto/Indicatore%3E?p?o}
 - LODE: **not yet implemented**
 - LodView: http://localhost:8080/lodview/onto/Indicatore 
 - LodLive: http://localhost/app_en.html?https://soilproject.org/onto/Indicatore

## Without Docker 
The ontologies files can still be created without using Docker by following the next steps.

### Virtual Environmment
It is suggested that developers interested in editing the project without Docker, 
do it in a safe virtual environment. Initializing a new python environment can 
be done in the following way:
```
$> python -m venv c:\path\to\myenv
```
Activating the python environment can be done in the following way:
```
$> source c:\path\to\myenv\bin\activate
```
#### Quick Example:
An example of python virtual environment initialization and activation could be:
```
python -m venv usr/bin/.kenv && source /usr/bin/.kenv/bin/activate
```

### Dependencies Installation
KE_Soil_Heritage requires Python 3.
Once the source code has been downladed it is possible to install its dependencies
by the means of pip using the *requirements.txt* in the *src* folder. For example:
```
pip install -r src/requirements.txt 
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
Congrats, now you have your data set up and ready to be used!

### Create Ontologies Files
All you need to do is navigate to the project *src* folder and run
the *main.py* script. Once it has finished all the computation, the ontologies
files will be stored in the *src/ontologies* folder.
