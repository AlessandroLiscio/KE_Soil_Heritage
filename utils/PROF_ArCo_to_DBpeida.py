from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.Wrapper import JSON
from rdflib import Graph
from rdflib.namespace import RDFS, RDF, OWL
from rdflib.term import URIRef, Literal

'''
 sparql -> it is any SELECT SPARQL query
 endpoint_url -> it is the URL of the target SPARQL endpoint,
 e.g. 'https://dati.beniculturali.it/sparql'
'''
def exect_select(sparql, endpoint_url):
    # We crete an instance of the SPARQLWrapper class
    wrapper = SPARQLWrapper(endpoint_url)
    
    # We set the SPARQL query we want to execute for the instance
    # of SPARQLWrapper we have created previously.
    wrapper.setQuery(sparql)
    
    wrapper.setReturnFormat(JSON)
    
    # We can query the endpoint
    query_execution = wrapper.query()
    
    # We convert the query execution into a result set
    result_set = query_execution.convert()
    
    return result_set
    
if __name__ == '__main__':
    
    arco_endpoint = 'https://dati.beniculturali.it/sparql'
    arco_sparql = '''
        SELECT ?arco_class ?arco_label
        WHERE {
            GRAPH <https://w3id.org/arco/ontology>{
                ?arco_class a owl:Class;
                    rdfs:label ?arco_label
                FILTER(LANG(?arco_label) = 'en')
            }
        }
    '''
    
    dbpedia_endpoint = 'http://semantics.istc.cnr.it/cordone/sparql'
    dbpedia_sparql = '''
        SELECT ?dbpedia_class ?dbpedia_label
        WHERE {
            GRAPH <https://dbpedia.org/ontology>{
                ?dbpedia_class a owl:Class;
                    rdfs:label ?dbpedia_label
                FILTER(LANG(?dbpedia_label) = 'en')
            }
        }
    '''
    
    
    arco_result_set = exect_select(arco_sparql, arco_endpoint)
    
    arco_solutions = [{'concept': binding["arco_class"]["value"], 'label': binding["arco_label"]["value"]} for binding in arco_result_set["results"]["bindings"]]
    
    dbpedia_result_set = exect_select(dbpedia_sparql, dbpedia_endpoint)
    
    dbpedia_solutions = [{'concept': binding["dbpedia_class"]["value"], 'label': binding["dbpedia_label"]["value"]} for binding in dbpedia_result_set["results"]["bindings"]]
    
    for arco_solution in arco_solutions:
        arco_class = arco_solution['concept']
        arco_label = arco_solution['label']
        for dbpedia_solution in dbpedia_solutions:
            dbpedia_class = dbpedia_solution['concept']
            dbpedia_label = dbpedia_solution['label']
            
            if arco_label.lower() == dbpedia_label.lower():
                print(arco_class, dbpedia_class)