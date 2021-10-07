import os
import re
import pandas as pd

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, DC, OWL
from rdflib.term import URIRef, Literal

###############################################################################
################################ PREFIXES #####################################
###############################################################################

# A good practice for creating IRIs is the following
#   {protocol}://{domain}/{format}/{enity type}/{entity key}
#
# Where:
# • protocol might be http, https, ftp, etc.
# • domain is the Web domain where the resource is available
# • format specifies the medium type. A limited number of values should be used
#     such as "doc" if the identified resource is a descriptive document,
#     "set" if the resource is a dataset, "id" or "item" if the
#     resource is a real world object
# • entity type refers to the class to which the instance belongs to,
#     e.g. Person, Organisation, CulturalProperty
# • entity key denotes a unique alphanumeric identifier of the instance,
#     e.g. the legal identifier of a public administration agency or
#     a post code (depending on the nature of the instance).

# Define useful prefixes
PROTOCOL = 'https'
DOMAIN = 'w3id.org/stlab/ke/lifo'
ET_ONTOLOGY = 'onto'
ET_ID = 'id'

lifo = Namespace(f"{PROTOCOL}://{DOMAIN}/{ET_ONTOLOGY}/")
lifo_id = Namespace(f"{PROTOCOL}://{DOMAIN}/{ET_ID}/")

###############################################################################
############################# BASELINE GRAPH ##################################
###############################################################################

# Load baseline graph created wiht protégé
print("######################################################################")
print(">>> Loading graph: baseline")
protege_graph = Graph().parse('./data/baseline.owl')

###############################################################################
############################# METRICS GRAPH ################################
###############################################################################

# Load metrics data
metrics_data = pd.read_csv(os.path.join('data', 'Descrizione_campi.csv'),
                              sep=";")[6:].reset_index(drop=True)

# Initialize indicators dictionary for mapping to the right classes in the baseline graph
metrics_dict = {
    'IndicatoreConsumoSuolo' : {
        'ids' : [1,2,3,4,5,6],
        'params': [],
        'params_regex': []
    },
    'IndicatoreConsumoSuoloAreeEUAP' : {
        'ids': [7,8,9,10],
        'params': [],
        'params_regex': []
    },
    'IndicatoreConsumoSuoloDistanzaCorpiIdrici' : {
        'ids': [11,12,13,14,15],
        'params': [ 'distanza' ],
        'params_regex': [r'in_\d+m|oltre_\d+m']
    },
    'IndicatoreConsumoSuoloDistanzaCosta' : {
        'ids': [16,17,18,19,20,21,22,23,24,25,26],
        'params': [ 'distanza' ],
        'params_regex': [r'\d+-\d+m|oltre_\d+m']
    },
    'IndicatoreConsumoSuoloQuota' : {
        'ids': [27,28,29,30,31,32,33,34,35],
        'params': [ 'distanza' ],
        'params_regex': [r'\d+-\d+m|oltre_\d+m']
    },
    'IndicatoreConsumoSuoloPendenza' : {
        'ids': [36,37,38,39,40,41],
        'params': [ 'pendenza' ],
        'params_regex': [r'\d+-\d+%|oltre_\d+%']
    },
    'IndicatoreConsumoSuoloPericolositàIdraulica' : {
        'ids': [42,43,44,45,46,47,48,49,50],
        'params': [ 'pericolosità idraulica' ],
        'params_regex': [r'\d']
    },
    'IndicatoreConsumoSuoloPericolositàFrane' : {
        'ids': [51,52,53,54,55,56,57,58,59,60,61,62,63,64,65],
        'params': [ 'pericolosità frane' ],
        'params_regex': [r'\d']
    },
    'IndicatoreConsumoSuoloPericolositàSismica': {
        'ids': [66,67,68,69,70,71],
        'params': [ 'pericolosità sismica' ],
        'params_regex': [r'alta|molto_alta']
    },
    'IndicatoreCopertureArtificiali' : {
        'ids': [72,73,74,75,76,77,78,79,80],
        'params': [ 'tipo superficie', 'distanza' ],
        'params_regex': [r'alterata|non_alterata',r'\dm']
    },
    'IndicatoreAreaCostruitaRispettoClasseDensità' : {
        'ids': [93,94,95,96],
        'params': [ 'distanza', 'classe area densità' ],
        'params_regex': [r'\dm', r'1|2_3']
    },
    'IndicatoreAreaClasseDensità' : {
        'ids':[97,98,99,100,101,102,103,104],
        'params': ['classe area densità'],
        'params_regex': [r'1|2|3|2_3']
    },
    'IndicatoreAltro' : {
        'ids': [81,82,83,84,85,86,88,88,89,90,91,92,
                105,106,107,108,109,
                110,111,112,113,114,115,116,117,118,119,120,121,122,123,
                124,125],
        'params': [],
        'params_regex': []
    }
}

# Create indicators graph
metrics_graph = Graph()

print(">>> Creating graph: metrics")
for i, row in metrics_data.iterrows():

    # Store fields in variables
    metric_id = row['Campo_ID'].lower()
    metric_name = row['Campo'].replace('_', ' ')
    metric_descr = row['Descrizione']

    # Find the indicator class by looking into the vocabulary
    for key in metrics_dict:
        if i+1 in metrics_dict[key]['ids']:
            metric_class = key
            break

   # rdf:type
    metrics_graph.add((
        URIRef(lifo_id.Metric +"/"+ metric_id),
        RDF.type,
        URIRef(lifo.Metric)
    ))
    # rdfs:label
    metrics_graph.add((
        URIRef(lifo_id.Metric +"/"+ metric_id),
        RDFS.label,
        Literal(metric_name)
    ))
    # rdfs:comment
    metrics_graph.add((
        URIRef(lifo_id.Metric +"/"+ metric_id),
        RDFS.comment,
        Literal(metric_descr)
    ))
    # lifo:MetricIdentifier
    metrics_graph.add((
        URIRef(lifo_id.Metric +"/"+ metric_id),
        lifo.MetricIdentifier,
        Literal(metric_id)
    ))
    # lifo:hasUnitMeasure
    indicator_metric = re.search('\[(.*?)\]', metric_descr)
    if indicator_metric is not None:
        metrics_graph.add((
            URIRef(lifo_id.Metric + "/" + metric_id),
            lifo.hasUnitMeasure,
            Literal(indicator_metric.group(0))
        ))

###############################################################################
############################### PLACES GRAPH ##################################
###############################################################################

# Create places graph
places_graph = Graph()
print(">>> Creating graph: places")

## Add Italy as country
# rdf:type
places_graph.add((
    URIRef(lifo_id.Country + "/italia"),
    RDF.type,
    URIRef(lifo.Country)
))
# rdfs:label
places_graph.add((
    URIRef(lifo_id.Country + "/italia"),
    RDFS.label,
    Literal("Italia")
))

# Populate places graph
for place in ['Regioni', 'Province', 'Comuni']:

    # Load data
    data = pd.read_csv(os.path.join('data', f'{place}_2015.csv'),
        sep=";", encoding='latin1')

    # Iterate
    for i, row in data.iterrows():

        # Store place code and name
        if place == 'Regioni':
            SHORT = 'REG'
            LONG = 'La regione'
            code = row['COD_REG']
            name = row['NOME_Regione']
            prefix_id = lifo_id.Region
            prefix_onto = lifo.Region
            isAdministrationOf = lifo_id.Country + '/' + 'italia'
        elif place == 'Province':
            SHORT = 'PRO'
            LONG = 'La provincia di'
            code = row['COD_PRO']
            name = row['NOME_Provincia']
            prefix_id = lifo_id.Province
            prefix_onto = lifo.Province
            isAdministrationOf = lifo_id.Region + '/' + row['NOME_Regione'].replace(' ', '-').lower()
        else:
            SHORT = 'COM'
            LONG = 'Il comune di'
            code = row['PRO_COM']
            name = row['NOME_Comune']
            prefix_id = lifo_id.City
            prefix_onto = lifo.City
            isAdministrationOf = lifo_id.Province + '/' + row['NOME_Provincia'].replace(' ', '-').lower()
        name = name.replace(' ', '-').lower()

        # rdf:type
        places_graph.add((
            URIRef(prefix_id + "/" + name),
            RDF.type,
            URIRef(prefix_onto)
        ))
        # rdfs:label
        places_graph.add((
            URIRef(prefix_id + "/" + name),
            RDFS.label,
            Literal(f"{name}")
        ))
        # lifo:isAdministrationOf
        places_graph.add((
            URIRef(prefix_id + "/" + name),
            lifo.isAdministrationOf,
            URIRef(isAdministrationOf)
        ))


adm_query = """
SELECT DISTINCT ?a ?b
WHERE { ?a lifo:isAdministrationOf ?b }
"""

places_graph.bind("lifo", lifo)
adm_qres = places_graph.query(adm_query)
for row in adm_qres:
    # lifo:hasAdministrationOf
    places_graph.add((
        URIRef(row[1]),
        lifo.hasAdministrationOf,
        URIRef(row[0])
    ))

## Ontology alignement for places
f = open('alignement/limes_places.txt')
for row in f.readlines():
    source, target, score = row.split('\t')
    # owl:sameAs
    places_graph.add((
        URIRef(source[1:-1]), # remove < and >
        OWL.sameAs,
        URIRef(target[1:-1]) # remove < and >
    ))

###############################################################################
####################### INDICATOR_COLLECTION GRAPH ############################
###############################################################################

# Create indicatorCollection graph
indicatorCollection_graph = Graph()

print(">>> Creating graph: indicatorCollection")
for year in ['2012', '2015']:
    # for place in ['Nazionale', 'Regioni']:
    for place in ['Nazionale', 'Regioni', 'Province']:
    # for place in ['Nazionale', 'Regioni', 'Province', 'Comuni']: # -> CAREFUL: 'Comuni' files are VERY big!

        # Load Data
        print(f'>>>>>> Working to {place} {year}')
        data = pd.read_csv(os.path.join('data', f'{place}_{year}.csv'),
                           sep=";", encoding='latin1') #encoding_errors='ignore')

        # For each row create a new instance of CollezioneIndicatori
        for i, row in data.iterrows():

            # Store place code and name
            if place == 'Regioni':
                SHORT = 'REG'
                LONG = 'La regione'
                code = row['COD_REG']
                name = row['NOME_Regione']
                prefix_id = lifo_id.Region
                prefix_onto = lifo.Region
            elif place == 'Province':
                SHORT = 'PRO'
                LONG = 'La provincia di'
                code = row['COD_PRO']
                name = row['NOME_Provincia']
                prefix_id = lifo_id.Province
                prefix_onto = lifo.Province
            elif place == 'Comuni':
                SHORT = 'COM'
                LONG = 'Il comune di'
                code = row['PRO_COM']
                name = row['NOME_Comune']
                prefix_id = lifo_id.City
                prefix_onto = lifo.City
            else:
                SHORT = 'ITA'
                LONG = 'la nazione'
                code = ''
                name = row['Nazione']
                prefix_id = lifo_id.Country
                prefix_onto = lifo.Country

            name = name.replace(' ', '-').lower()

            ##########################
            # PLACE-YEAR COLLECTIONS #
            ##########################

            # store indicator_collection suffix
            indicator_collection = f"/{SHORT}{code}_{year}"

            # rdfs:type
            indicatorCollection_graph.add((
                URIRef(lifo_id.IndicatorsCollection + indicator_collection),
                RDF.type,
                URIRef(lifo.IndicatorsCollection)
                ))
            # rdfs:label
            indicatorCollection_graph.add((
                URIRef(lifo_id.IndicatorsCollection + indicator_collection),
                RDFS.label,
                Literal(f"Consumo del suolo per {LONG} {name} nell'anno {year}")
                ))

            # lifo:hasLocation
            indicatorCollection_graph.add((
                URIRef(lifo_id.IndicatorsCollection + indicator_collection),
                lifo.hasLocation,
                URIRef(prefix_id + "/" + name)
            ))
            # dc:date
            indicatorCollection_graph.add((
                URIRef(lifo_id.IndicatorsCollection + indicator_collection),
                DC.date,
                Literal(year)
                ))

            for metric in metrics_data['Campo_ID']:

                # Avoid 'C7' indicator:
                # - Regioni -> C7_RM_1956;C7_RM_1989;C7_RM_1998;C7_RM_2008;C7_RM_2013
                # - Comuni e Province -> Does not exist
                if metric == 'C7': continue

                ##################################
                # PLACE-YEAR METRIC #
                ##################################

                indicator_entity = f"/{SHORT}{code}_{year}_{metric.lower()}"

                # rdfs:label
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    RDF.type,
                    lifo.Indicator
                    ))

                # rdfs:label
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    RDFS.label,
                    Literal(indicator_collection[1:] + f"_{metric}")
                    ))
                # lifo:measuredBy
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    lifo.measuredBy,
                    URIRef(lifo_id + "Metric/" + metric.lower())
                    ))
                # rdfs:comment
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    RDFS.comment,
                    Literal(f"{metrics_data[metrics_data['Campo_ID'] == metric]['Descrizione'].to_list()[0]} per {name} nell'anno {year}")
                    ))
                # lifo:isPartOf
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    lifo.isPartOf,
                    URIRef(lifo_id.IndicatorsCollection + indicator_collection)
                    ))
                # rdf:value
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    RDF.value,
                    Literal(str(row[metric]).replace(',','.'))
                    ))
                # lifo:hasLocation
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    lifo.hasLocation,
                    URIRef(prefix_id + "/" + name)
                ))
                # dc:date
                indicatorCollection_graph.add((
                    URIRef(lifo_id.Indicator + indicator_entity),
                    DC.date,
                    Literal(year)
                    ))

###############################################################################
################################ OUTPUT #######################################
###############################################################################

# Merge graphs
final_graph = protege_graph + places_graph + metrics_graph + indicatorCollection_graph
final_graph.bind("lifo", lifo)
final_graph.bind("rdf", RDF)
final_graph.bind("rdfs", RDFS)
final_graph.bind("dc", DC)
print("######################################################################")
print(">>> protege graph statements: {}".format(len(protege_graph)))
print(">>> indicators graph statements: {}".format(len(metrics_graph)))
print(">>> indicatorCollection graph statements: {}".format(len(indicatorCollection_graph)))
print(">>>>>> final graph statements: {}".format(len(final_graph)))
print("######################################################################")

# Serialize graph to .ttl files
if not os.path.isdir('./ontologies'): os.mkdir('./ontologies')
final_graph.serialize(destination='./ontologies/final_graph.ttl', format='turtle')
