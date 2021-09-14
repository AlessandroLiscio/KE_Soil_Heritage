// LodLive will match connection by the base URL of the query used, so the key must match the URL
$.jStorage.set(
'profile', {
  // endpoint connection parameters
  'connection' : {
    // http matches all http requests, so this will be the only connection settings used
   'http:' : {
          description : {
          en : 'soilproject.org',
          it : 'soilproject.org',
        },
        sparql : {
          allclasses : 'select distinct ?object  where {[] a ?object} order by ?object  limit 50  ',
          findsubject : 'select distinct ?subject where { {?subject a <{class}>;<http://purl.org/dc/elements/1.1/title> ?object. filter(regex(str(?object),\'{value}\',\'i\'))} union {?subject a <{class}>;<http://www.w3.org/2000/01/rdf-schema#label> ?object. filter(regex(str(?object),\'{value}\',\'i\'))} union {?subject a <{class}>;<http://www.w3.org/2004/02/skos/core#preflabel> ?object. filter(regex(str(?object),\'{value}\',\'i\'))} } limit 1',
          documenturi : 'select distinct * where {<{uri}> ?property ?object.filter ((( isiri(?object) && ?property != <http://xmlns.com/foaf/0.1/depiction> )|| ?property = <http://www.w3.org/2000/01/rdf-schema#label>  || ?property = <http://www.georss.org/georss/point> || ?property = <http://xmlns.com/foaf/0.1/surname> || ?property = <http://xmlns.com/foaf/0.1/name> || ?property = <http://purl.org/dc/elements/1.1/title>))}  order by ?property',
          document : 'select distinct *  where  {{<{uri}> ?property ?object. filter(!isliteral(?object))} union    {<{uri}> ?property    ?object.filter(isliteral(?object)).filter(lang(?object) ="it")} union   {<{uri}> ?property    ?object.filter(isliteral(?object)).filter(lang(?object) ="en")}}  order by ?property',
          bnode : 'select distinct *  where {<{uri}> ?property ?object}',
          inverse : 'select distinct * where {?object ?property <{uri}> filter(regex(str(?object),\'//dbpedia.org\'))} limit 100',
          inversesameas : 'select distinct * where {?object <http://www.w3.org/2002/07/owl#sameas> <{uri}> filter(regex(str(?object),\'//dbpedia.org\'))}'
        },
        useforinversesameas : true,
     endpoint : 'http://localhost:8890/sparql',
        examples : [{
          label : 'Indicatore',
          uri : 'https://soilproject.org/onto/indicatore'
        }, {
          label : 'CollezioneIndicatori',
          uri : 'https://soilproject.org/onto/CollezioneIndicatori'
			}]
    },
    // here we define the known relationships so that labels will appear
    arrows : {
      'http://www.w3.org/2002/07/owl#sameas' : 'issameas',
      'http://purl.org/dc/terms/ispartof' : 'ispartof',
      'http://purl.org/dc/elements/1.1/type' : 'istype',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' : 'istype',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#subclassof' : 'issubclassof'
    };
  };
  // this is the default data configuration, this is important.  it informs lodlive how to construct queries and how to read the data that comes back
  'default' = {
    sparql : {
      allclasses : 'select distinct ?object where {[] a ?object}',
      findsubject : 'select distinct ?subject where { {?subject a <{class}>;<http://purl.org/dc/elements/1.1/title> ?object. filter(regex(str(?object),\'{value}\',\'i\'))} union {?subject a <{class}>;<http://www.w3.org/2000/01/rdf-schema#label> ?object. filter(regex(str(?object),\'{value}\',\'i\'))} union {?subject a <{class}>;<http://www.w3.org/2004/02/skos/core#preflabel> ?object. filter(regex(str(?object),\'{value}\',\'i\'))} }  limit 1  ',
      documenturi : 'select distinct * where {<{uri}> ?property ?object} order by ?property',
      document : 'select distinct * where {<{uri}> ?property ?object}',
      bnode : 'select distinct *  where {<{uri}> ?property ?object}',
      inverse : 'select distinct * where {?object ?property <{uri}>.} limit 100',
      inversesameas : 'select distinct * where {{?object <http://www.w3.org/2002/07/owl#sameas> <{uri}> } union { ?object <http://www.w3.org/2004/02/skos/core#exactmatch> <{uri}>}}'
    },
    endpoint : 'http://labs.regesta.com/resourceproxy/',
    document : {
      classname : 'standard',
      titlename: 'none',
      titleproperties : ['http://xmlns.com/foaf/0.1/name']
    }, // http://www.w3.org/2000/01/rdf-schema#label
  };
});

'endpoints' = {
  all : 'output=json&format=json&timeout=0',
  jsonp: true
};
