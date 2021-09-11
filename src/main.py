from pyrml import RMLConverter
import os
import pandas as pd
from rdflib import Graph
from rdflib.namespace import RDF, RDFS, SKOS, FOAF, DC
from rdflib.term import URIRef, Literal

#TODO:
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
PREFIX_SOILPROJECT = "https://soilproject.org/onto"

PREFIX_ATTRIBUTES = PREFIX_SOILPROJECT+"/attributi"
PREFIX_REG_YEAR_COLLECTION = PREFIX_SOILPROJECT+"/CollezioneIndicatori"
PREFIX_INDICATOR = PREFIX_SOILPROJECT+"/Indicatore"
PREFIX_TEMP = PREFIX_SOILPROJECT+"TEMP#"

#TODO: remove this prefixes from ontology
PREFIX_ISPRA_CORE = "http://dati.isprambiente.it/ontology/core#"
PREFIX_ISPRA_PLACES = "http://dati.isprambiente.it/id/place/"

# start from protégé graph
protege_graph = Graph().parse('./data/webprotege.owl')

# Create Indicators Ontology
indicators_data = pd.read_csv(os.path.join('data', f'Descrizione_campi.csv'), sep=";")[6:]
indicators_graph = Graph()

for i, row in indicators_data.iterrows():

    # Store fields in variables
    indicator_id = row['Campo_ID']
    indicator_name = row['Campo']
    indicator_descr = row['Descrizione']

    # Indicator class
    indicators_graph.add((
        URIRef(PREFIX_INDICATOR + f"/{indicator_id}"),
        URIRef(RDF.type),
        Literal(PREFIX_INDICATOR)
    ))
    # Indicator label
    indicators_graph.add((
        URIRef(PREFIX_INDICATOR + f"/{indicator_id}"),
        URIRef(RDFS.label),
        Literal(indicator_id)
    ))
    # # Indicator name
    # indicators_graph.add((
    #     URIRef(PREFIX_INDICATOR + f"/{indicator_id}"),
    #     URIRef(),
    #     Literal(indicator_name)
    # ))
    # Indicator description
    indicators_graph.add((
        URIRef(PREFIX_INDICATOR + f"/{indicator_id}"),
        URIRef(RDFS.comment),
        Literal(indicator_descr)
    ))

#
# python_graph = Graph()
# for year in ['2012', '2015']:
#     for target in ['Regioni']:
#     # for target in ['Regioni', 'Province']:
#     # for target in ['Regioni', 'Province', 'Comuni']: # -> CAREFUL: 'Comuni' files are VERY big!
#
#         print(f'Working on {target}_{year}.csv')
#         # Load Data
#         data = pd.read_csv(os.path.join('data', f'{target}_{year}.csv'), sep=";", encoding='latin1') #encoding_errors='ignore')
#
#         for i, row in data.iterrows():
#
#             # Store target code and name
#             if target == 'Regioni':
#                 short = 'REG'
#                 long = 'la regione'
#                 code = row['COD_REG']
#                 name = row['NOME_Regione']
#             elif target == 'Province':
#                 short = 'PRO'
#                 long = 'la provincia di'
#                 code = row['COD_PRO']
#                 name = row['NOME_Provincia']
#             else:
#                 short = 'COM'
#                 long = 'il comune di'
#                 code = row['PRO_COM']
#                 name = row['NOME_Comune']
#             name_refactored = name.replace(' ','-').lower()
#
#
#             ###########################
#             # REGION-YEAR COLLECTIONS #
#             ###########################
#             # rdfs:label
#             python_graph.add((
#                 URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
#                 URIRef(RDFS.label),
#                 Literal(f"Consumo del suolo per {long} {name} nell'anno {year}")
#                 ))
#             # rdfs:type
#             python_graph.add((
#                 URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
#                 URIRef(RDF.type),
#                 URIRef(PREFIX_ISPRA_CORE + "IndicatorCollection")
#                 ))
#             # foaf:PrimaryTopic
#             python_graph.add((
#                 URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
#                 URIRef(FOAF.PrimaryTopic),
#                 URIRef(PREFIX_ISPRA_PLACES + name_refactored)
#                 ))
#             # dc:date
#             python_graph.add((
#                 URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
#                 URIRef(DC.date),
#                 Literal(year)
#                 ))
#
#             for indicator in indicators_data['Campo_ID']:
#
#                 # Avoid 'C7' indicator:
#                 # - Regioni -> C7_RM_1956;C7_RM_1989;C7_RM_1998;C7_RM_2008;C7_RM_2013
#                 # - Comuni e Province -> Does not exist
#                 if indicator == 'C7': continue;
#
#                 ##################################
#                 # TARGET-YEAR-INDICATOR ENTITIES #
#                 ##################################
#                 # rdfs:label
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(RDFS.label),
#                     Literal(f"{short}{code}_{year}_{indicator}")
#                     ))
#                 # rdfs:comment (Description)
#
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(RDFS.comment),
#                     Literal(f"{indicators_data[indicators_data['Campo_ID'] == indicator]['Descrizione'].to_list()[0]} per {name} nell'anno {year}")
#                     ))
#                 # dc:isPartOf -> (TARGET-YEAR collection)
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(DC.isPartOf),
#                     URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}")
#                     ))
#                 # dc:type
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(DC.type),
#                     URIRef(PREFIX_ATTRIBUTES + indicator.lower())
#                     ))
#                 # rdf:value -> from table
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(RDF.value),
#                     Literal(row[indicator])
#                     ))
#                 # foaf:PrimaryTopic
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(FOAF.PrimaryTopic),
#                     URIRef(PREFIX_ISPRA_PLACES + name_refactored)
#                     ))
#                 # dc:date
#                 python_graph.add((
#                     URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
#                     URIRef(DC.date),
#                     Literal(year)
#                     ))
#
#
# Print graph lengths
print("protege_graph has {} statements.".format(len(protege_graph)))
print("indicators_graph has {} statements.".format(len(indicators_graph)))
# print("python_graph has {} statements.".format(len(python_graph)))


# Merge graphs
final_graph = protege_graph + indicators_graph # + python_graph
print("final_graph has {} statements.".format(len(final_graph)))
# final_graph.serialize(destination='./ontologies/final_graph.ttl', format='turtle')
#
# Serialize graphs to .ttl files
os.mkdir('./ontologies')
protege_graph.serialize(destination='./ontologies/protege_graph.ttl', format='turtle')
indicators_graph.serialize(destination='./ontologies/indicators_graph.ttl', format='turtle')
# python_graph.serialize(destination='./ontologies/python_graph.ttl', format='turtle')

# # Print the triples contained into the RDF graph.
# for s, p, o in final_graph:
#     print(s, p, o)

# ###########
# # QUERIES #
# ###########
# qres = final_graph.query(
#     """SELECT ?s ?o
#         WHERE
#             { ?s rdfs:label ?o }""")
#
# print("###################################")
# for row in qres:
#     print("%s %s" % row)
# print("###################################")
