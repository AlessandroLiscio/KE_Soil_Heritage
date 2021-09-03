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
rdf_attribute_graph = rml_converter.convert(rml_attribute_file_path)

# REGIONS
rml_region_file_path = os.path.join('mappings', 'region-map.ttl')
rdf_region_graph = rml_converter.convert(rml_region_file_path)

# Merge graphs
final_graph = rdf_attribute_graph + rdf_region_graph

# Define useful prefixes
PREFIX_ATTRIBUTES = "http://soilproject/id/skos/sc/"
PREFIX_REG_YEAR_COLLECTION = "https://soilproject/id/collection/sc/"
PREFIX_INDICATORS = "https://soilproject/id/indicator/sc/"
PREFIX_TEMP = "https://soilproject/temp#"

PREFIX_ISPRA_CORE = "http://dati.isprambiente.it/ontology/core#"
PREFIX_ISPRA_PLACES = "http://dati.isprambiente.it/id/place/"

# Get all the attributes useful information by querying the graph
attributes_data = pd.read_csv(os.path.join('data', f'Descrizione_campi.csv'), sep=";")
attributes_data = attributes_data[6:]

for year in ['2012', '2015']:
    for target in ['Regioni']:
    # for target in ['Regioni', 'Province']:
    # for target in ['Regioni', 'Province', 'Comuni']: # -> CAREFUL: 'Comuni' files are VERY big!

        print(f'Working on {target}_{year}.csv')
        # Load Data
        data = pd.read_csv(os.path.join('data', f'{target}_{year}.csv'), sep=";", encoding_errors='ignore')

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
>>>>>>> 48521f0 (typo fix)
                    URIRef(RDFS.label),
                    Literal("Consumo del suolo nella regione " + f"{region_name} nell'anno {year}")
        ))
        final_graph.add(( 
                    URIRef(PREFIX_REG_YEAR_COLLECTION + f"REG{region_code}_{year}"),
                    URIRef(RDF.type),
                    URIRef(PREFIX_ISPRA_CORE + "IndicatorCollection")
        ))
        final_graph.add(( 
                    URIRef(PREFIX_REG_YEAR_COLLECTION + f"REG{region_code}_{year}"),
                    URIRef(FOAF.PrimaryTopic),
                    URIRef(PREFIX_ISPRA_PLACES + region_name_refactored)
        ))
        final_graph.add(( 
                    URIRef(PREFIX_REG_YEAR_COLLECTION + f"REG{region_code}_{year}"),
                    URIRef(DC.date),
                    Literal(year)
        ))
        
        for j in range(0, len(attributes_data['Campo_ID'])):

            indicator = attributes_data.iloc[j]['Campo_ID'].lower()

            final_graph.add(( 
                        URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                        URIRef(RDFS.label),
                        Literal(f"REG{region_code}_{year}_{indicator.upper()}")
                        ))
            index = attributes_data.index[attributes_data['Campo_ID'] == indicator.upper()]
            if len(index) > 0:
                index = index[0]-6
                final_graph.add(( 
                            URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                            URIRef(RDFS.comment),
                            Literal(f"{attributes_data.iloc[index]['Descrizione']} per la regione {region_name} nell'anno {year}")
                        ))
            final_graph.add(( 
                        URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                        URIRef(DC.isPartOf),
                        URIRef(PREFIX_REG_YEAR_COLLECTION + f"REG{region_code}_{year}")
                        ))
            final_graph.add(( 
                        URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                        URIRef(DC.type),
                        URIRef(PREFIX_ATTRIBUTES + indicator)
                        ))
            final_graph.add(( 
                        URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                        URIRef(RDF.value),
                        Literal(row[j+2])
                        ))
            final_graph.add(( 
                        URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                        URIRef(FOAF.PrimaryTopic),
                        URIRef(PREFIX_ISPRA_PLACES + region_name_refactored)
                        ))
            final_graph.add(( 
                        URIRef(PREFIX_INDICATORS + f"REG{region_code}_{year}_{indicator}"),
                        URIRef(DC.date), 
                        Literal(year)
                        ))

# Print the triples contained into the RDF graph.
# for s, p, o in final_graph:
#     print(s, p, o)

final_graph.serialize(destination='output.ttl', format='turtle')
print("graph has {} statements.".format(len(final_graph)))

# qres = final_graph.query(
#     """SELECT ?name ?ha
#         WHERE
#             { ?place rdfs:label ?name ;
#             <https://lisciofortini/attribute/C1> ?ha .}""")
# 
# qres = final_graph.query(
#     """SELECT ?name ?d ?v
#         WHERE
#             { ?place rdfs:label ?name ;
#                     ?s ?v.
#                 ?s <http://prova.attribute.ex/att#descrizione> ?d.
#                 FILTER regex(?name, "^Emilia").}""")
# 
# qres = final_graph.query(
#     """SELECT ?attr ?d
#         WHERE
#             { ?attr <http://prova.attribute.ex/att#descrizione> ?d}""")
# 
# # Get all the attributes useful information by querying the graph
# qres = final_graph.query(
#     """SELECT DISTINCT ?descr
#         WHERE {
#             ?id <http://prova.attribute.ex/att#descrizione> ?descr
#         }""")

# print("###################################")
# for row in qres:
#     print("%s %s %s" % row)
# print("###################################")
