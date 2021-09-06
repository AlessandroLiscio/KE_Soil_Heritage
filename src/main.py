from pyrml import RMLConverter
import os
import pandas as pd
from rdflib.namespace import RDF, RDFS, SKOS, FOAF, DC
from rdflib.term import URIRef, Literal

# Create an instance of the class RMLConverter.
rml_converter = RMLConverter()

'''
Invoke the method convert on the instance of class RMLConverter by:
 - using the file examples/artist/artist-map.ttl (see the examples in this repo);
 - obtaining an RDF graph as output.
'''

# ATTRIBUTES
rml_attribute_file_path = os.path.join('mappings', 'attribute-map.ttl')
g = rml_converter.convert(rml_attribute_file_path)

# Define useful prefixes
PREFIX_ATTRIBUTES = "https://soilproject.org/onto/id/skos/sc/"
PREFIX_REG_YEAR_COLLECTION = "https://soilproject.org/onto/id/collection/sc/"
PREFIX_INDICATORS = "https://soilproject.org/onto/id/indicator/sc/"
PREFIX_TEMP = "https://soilproject.org/onto/temp#"

PREFIX_ISPRA_CORE = "http://dati.isprambiente.it/ontology/core#"
PREFIX_ISPRA_PLACES = "http://dati.isprambiente.it/id/place/"

# Get all the indicators useful information
indicators_data = pd.read_csv(os.path.join('data', f'Descrizione_campi.csv'), sep=";")[6:]

for year in ['2012', '2015']:
    for target in ['Regioni']:
    # for target in ['Regioni', 'Province']:
    # for target in ['Regioni', 'Province', 'Comuni']: # -> CAREFUL: 'Comuni' files are VERY big!

        print(f'Working on {target}_{year}.csv')
        # Load Data
        data = pd.read_csv(os.path.join('data', f'{target}_{year}.csv'), sep=";", encoding='latin1') #encoding_errors='ignore')

        for i, row in data.iterrows():

            # Store target code and name
            if target == 'Regioni':
                short = 'REG'
                long = 'la regione'
                code = row['COD_REG']
                name = row['NOME_Regione']
            elif target == 'Province':
                short = 'PRO'
                long = 'la provincia di'
                code = row['COD_PRO']
                name = row['NOME_Provincia']
            else:
                short = 'COM'
                long = 'il comune di'
                code = row['PRO_COM']
                name = row['NOME_Comune']
            name_refactored = name.replace(' ','-').lower()


            ###########################
            # REGION-YEAR COLLECTIONS #
            ###########################
            # rdfs:label
            g.add(( 
                URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
                URIRef(RDFS.label),
                Literal(f"Consumo del suolo per {long} {name} nell'anno {year}")
                ))
            # rdfs:type
            g.add(( 
                URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
                URIRef(RDF.type),
                URIRef(PREFIX_ISPRA_CORE + "IndicatorCollection")
                ))
            # foaf:PrimaryTopic
            g.add(( 
                URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
                URIRef(FOAF.PrimaryTopic),
                URIRef(PREFIX_ISPRA_PLACES + name_refactored)
                ))
            # dc:date
            g.add(( 
                URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}"),
                URIRef(DC.date),
                Literal(year)
                ))
            
            for indicator in indicators_data['Campo_ID']:

                # Avoid 'C7' indicator:
                # - Regioni -> C7_RM_1956;C7_RM_1989;C7_RM_1998;C7_RM_2008;C7_RM_2013
                # - Comuni e Province -> Does not exist
                if indicator == 'C7': continue;

                ##################################
                # TARGET-YEAR-INDICATOR ENTITIES #
                ##################################
                # rdfs:label
                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(RDFS.label),
                    Literal(f"{short}{code}_{year}_{indicator}")
                    ))
                # rdfs:comment (Description)

                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(RDFS.comment),
                    Literal(f"{indicators_data[indicators_data['Campo_ID'] == indicator]['Descrizione'].to_list()[0]} per {name} nell'anno {year}")
                    ))
                # dc:isPartOf -> (TARGET-YEAR collection)
                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(DC.isPartOf),
                    URIRef(PREFIX_REG_YEAR_COLLECTION + f"{short}{code}_{year}")
                    ))
                # dc:type
                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(DC.type),
                    URIRef(PREFIX_ATTRIBUTES + indicator.lower())
                    ))
                # rdf:value -> from table
                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(RDF.value),
                    Literal(row[indicator])
                    ))
                # foaf:PrimaryTopic
                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(FOAF.PrimaryTopic),
                    URIRef(PREFIX_ISPRA_PLACES + name_refactored)
                    ))
                # dc:date
                g.add(( 
                    URIRef(PREFIX_INDICATORS + f"{short}{code}_{year}_{indicator.lower()}"),
                    URIRef(DC.date), 
                    Literal(year)
                    ))

print("graph has {} statements.".format(len(g)))
os.mkdir('./ontologies')
g.serialize(destination='./ontologies/output.ttl', format='turtle')

# Print the triples contained into the RDF graph.
# for s, p, o in g:
#     print(s, p, o)
#
# ###########
# # QUERIES #
# ###########
# qres = g.query(
#     """SELECT ?s ?o
#         WHERE
#             { ?s rdfs:label ?o }""")
# 
# qres = g.query(
#     """SELECT ?name ?d ?v
#         WHERE
#             { ?place rdfs:label ?name ;
#                     ?s ?v.
#                 ?s <http://prova.attribute.ex/att#descrizione> ?d.
#                 FILTER regex(?name, "^Emilia").}""")
# 
# qres = g.query(
#     """SELECT ?attr ?d
#         WHERE
#             { ?attr <http://prova.attribute.ex/att#descrizione> ?d}""")
# 
# # Get all the attributes useful information by querying the graph
# qres = g.query(
#     """SELECT DISTINCT ?descr
#         WHERE {
#             ?id <http://prova.attribute.ex/att#descrizione> ?descr
#         }""")
#
# print("###################################")
# for row in qres:
#     print("%s %s" % row)
# print("###################################")
