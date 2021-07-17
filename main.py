from pyrml import RMLConverter
import os

# Create an instance of the class RMLConverter.
rml_converter = RMLConverter()

'''
Invoke the method convert on the instance of class RMLConverter by:
 - using the file examples/artist/artist-map.ttl (see the examples in this repo);
 - obtaining an RDF graph as output.
'''
rml_attribute_file_path = os.path.join('mappings', 'attribute-map.ttl')
rdf_attribute_graph = rml_converter.convert(rml_attribute_file_path)

rml_region_file_path = os.path.join('mappings', 'region-map.ttl')
rdf_region_graph = rml_converter.convert(rml_region_file_path)

# Print the triples contained into the RDF graph.
for s, p, o in rdf_attribute_graph:
    print(s, p, o)

print("graph has {} statements.".format(len(rdf_region_graph)))

qres = rdf_region_graph.query(
    """SELECT ?name ?ha
        WHERE
            { ?place rdfs:label ?name ;
            <https://lisciofortini/attribute/C1> ?ha}""")

for row in qres:
    print("%s has %s covered" % row)
