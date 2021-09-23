import pandas as pd
import os
import re

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, SKOS, FOAF, DC
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
DOMAIN = 'soilproject.org'
ET_ONTOLOGY = 'onto'
ET_ID = 'id'

sp_onto = Namespace(f"{PROTOCOL}://{DOMAIN}/{ET_ONTOLOGY}/")
sp_id = Namespace(f"{PROTOCOL}://{DOMAIN}/{ET_ID}/")
temp = Namespace(f"{PROTOCOL}://{DOMAIN}/temp/")

###############################################################################
############################# BASELINE GRAPH ##################################
###############################################################################

# Load baseline graph created wiht protégé
print("######################################################################")
print(">>> Loading graph: baseline")
protege_graph = Graph().parse('./data/baseline.owl')

###############################################################################
############################# INDICATORS GRAPH ################################
###############################################################################

# Load indicators data
indicators_data = pd.read_csv(os.path.join('data', 'Descrizione_campi.csv'),
                              sep=";")[6:].reset_index(drop=True)

# Initialize indicators dictionary for mapping to the right classes in the baseline graph
indicators_dict = {
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
indicators_graph = Graph()

print(">>> Creating graph: indicators")
for i, row in indicators_data.iterrows():
    
    # Store fields in variables
    indicator_id = row['Campo_ID'].lower()
    indicator_name = row['Campo'].replace('_', ' ')
    indicator_descr = row['Descrizione']

    # Find the indicator class by looking into the vocabulary
    for key in indicators_dict:
        if (i+1) in indicators_dict[key]['ids']:
            indicator_class = key
            break

   # rdf:type
    indicators_graph.add((
        URIRef(sp_id.Indicatore +"/"+ indicator_id),
        RDF.type,
        URIRef(sp_onto + indicator_class)
    ))
    # rdfs:label
    indicators_graph.add((
        URIRef(sp_id.Indicatore +"/"+ indicator_id),
        RDFS.label,
        Literal(indicator_name)
    ))
    # rdfs:comment
    indicators_graph.add((
        URIRef(sp_id.Indicatore +"/"+ indicator_id),
        RDFS.comment,
        Literal(indicator_descr)
    ))
    # temp:identificatore
    indicators_graph.add((
        URIRef(sp_id.Indicatore +"/"+ indicator_id),
        URIRef(temp + "/identificatore"),
        Literal(indicator_id)
    ))
    # temp:metrica
    indicator_metric = re.search('\[(.*?)\]', indicator_descr)
    if indicator_metric is not None:
        indicators_graph.add((
            URIRef(sp_id.Indicatore + "/" + indicator_id),
            URIRef(temp + "/metrica"),
            Literal(indicator_metric.group(0))
        ))
    # Indicator parameters
    for j, param in enumerate(indicators_dict[indicator_class]['params']):
        # Find the indicator parameter value by using a regex
        param_value = re.search(indicators_dict[key]['params_regex'][j], indicator_name)
        if param_value is not None:
            indicators_graph.add((
                URIRef(sp_id.Indicatore + "/" + indicator_id),
                URIRef(temp + "/" + param.replace(' ','_')),
                Literal(param_value.group(0).replace('_',' '))
            ))

###############################################################################
####################### INDICATOR_COLLECITON GRAPH ############################
###############################################################################

# Create indicatorCollection graph
indicatorCollection_graph = Graph()

print(">>> Creating graph: indicatorCollection")
for year in ['2012', '2015']:
    for place in ['Regioni']:
    # for place in ['Regioni', 'Province']:
    # for place in ['Regioni', 'Province', 'Comuni']: # -> CAREFUL: 'Comuni' files are VERY big!

        # Load Data
        print(f'>>>>>> Working to {place} {year}')
        data = pd.read_csv(os.path.join('data', f'{place}_{year}.csv'),
                           sep=";", encoding='latin1') #encoding_errors='ignore')

        # For each row create a new instance of CollezioneIndicatori
        for i, row in data.iterrows():

            # Store place code and name
            if place == 'Regioni':
                SHORT = 'REG'
                LONG = 'la regione'
                code = row['COD_REG']
                name = row['NOME_Regione']
            elif place == 'Province':
                SHORT = 'PRO'
                LONG = 'la provincia di'
                code = row['COD_PRO']
                name = row['NOME_Provincia']
            else:
                SHORT = 'COM'
                LONG = 'il comune di'
                code = row['PRO_COM']
                name = row['NOME_Comune']
            name_refactored = name.replace(' ','-').lower()

            ##########################
            # PLACE-YEAR COLLECTIONS #
            ##########################

            indicator_collection = f"/{SHORT}{code}_{year}"

            # rdfs:type
            indicatorCollection_graph.add((
                URIRef(sp_id.CollezioneIndicatori + indicator_collection),
                RDF.type,
                URIRef(sp_onto.CollezioneIndicatori)
                ))
            # rdfs:label
            indicatorCollection_graph.add((
                URIRef(sp_id.CollezioneIndicatori + indicator_collection),
                RDFS.label,
                Literal(f"Consumo del suolo per {LONG} {name} nell'anno {year}")
                ))
            # foaf:PrimaryTopic
            indicatorCollection_graph.add((
                URIRef(sp_id.CollezioneIndicatori + indicator_collection),
                FOAF.PrimaryTopic,
                URIRef(sp_onto.Luogo + "/" + name_refactored)
                ))
            # dc:date
            indicatorCollection_graph.add((
                URIRef(sp_id.CollezioneIndicatori + indicator_collection),
                DC.date,
                Literal(year)
                ))

            for indicator in indicators_data['Campo_ID']:

                # Avoid 'C7' indicator:
                # - Regioni -> C7_RM_1956;C7_RM_1989;C7_RM_1998;C7_RM_2008;C7_RM_2013
                # - Comuni e Province -> Does not exist
                if indicator == 'C7': continue;

                ##################################
                # PLACE-YEAR-INDICATOR ENTITIES #
                ##################################

                indicator_entity = f"/{SHORT}{code}_{year}_{indicator.lower()}"

                # rdfs:label
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    RDFS.label,
                    Literal(indicator_collection[1:] + f"_{indicator}")
                    ))
                # dc:type
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    DC.type,
                    URIRef(temp + "/" + indicator.lower())
                    ))
                # rdfs:comment
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    RDFS.comment,
                    Literal(f"{indicators_data[indicators_data['Campo_ID'] == indicator]['Descrizione'].to_list()[0]} per {name} nell'anno {year}")
                    ))
                # dc:isPartOf
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    DC.isPartOf,
                    URIRef(sp_id.CollezioneIndicatori + indicator_collection)
                    ))
                # rdf:value
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    RDF.value,
                    Literal(row[indicator])
                    ))
                # foaf:PrimaryTopic
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    FOAF.PrimaryTopic,
                    URIRef(sp_onto.Luogo + "/" + name_refactored)
                    ))
                # dc:date
                indicatorCollection_graph.add((
                    URIRef(sp_id.Indicatore + indicator_entity),
                    DC.date,
                    Literal(year)
                    ))


###############################################################################
################################ OUTPUT #######################################
###############################################################################

# Merge graphs
final_graph = protege_graph  + indicators_graph + indicatorCollection_graph
final_graph.bind("sp-onto", sp_onto)
final_graph.bind("sp-id", sp_id)
final_graph.bind("rdf", RDF)
final_graph.bind("rdfs", RDFS)
final_graph.bind("foaf", FOAF)
final_graph.bind("dc", DC)
print("######################################################################")
print(">>> protege graph statements: {}".format(len(protege_graph)))
print(">>> indicators graph statements: {}".format(len(indicators_graph)))
print(">>> indicatorCollection graph statements: {}".format(len(indicatorCollection_graph)))
print(">>>>>> final graph statements: {}".format(len(final_graph)))
print("######################################################################")

# Serialize graph to .ttl files
if not os.path.isdir('./ontologies'): os.mkdir('./ontologies')
final_graph.serialize(destination='./ontologies/final_graph.ttl', format='turtle')

###############################################################################
############################# EXAMPLE QUERY ###################################
###############################################################################

# QUERY = "SELECT DISTINCT ?s WHERE { ?s ?p ?o }"
# qres = final_graph.query(QUERY)
# print(">>> Query: ", QUERY)
# for row in qres: print("%s" % row)
# print("######################################################################")
