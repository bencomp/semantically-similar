from flask import Flask
import requests
app = Flask(__name__)

from SPARQLWrapper import SPARQLWrapper
with open('query-nmvw.rq') as q_file:
    queryString = q_file.read()

SPARQL_ENDPOINT_NMVW = "https://api.data.netwerkdigitaalerfgoed.nl/datasets/ivo/NMVW/services/NMVW-01/sparql"
SPARQL_ENDPOINT_RIJKS = "https://api.data.netwerkdigitaalerfgoed.nl/datasets/hackalod/RM-PublicDomainImages/services/RM-PublicDomainImages/sparql"

nmvw = SPARQLWrapper(SPARQL_ENDPOINT_NMVW)
# add a default graph, though that can also be part of the query string
# nmvw.addDefaultGraph("http://www.example.org/graph-selected")
nmvw.setQuery(queryString)
try :
    ret = nmvw.query()
   # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
except :
#    deal_with_the_exception()
    pass


@app.route('/year/<uri>')
def year(uri):
    return queryString.format(uri)
    # return "bar based on year"

@app.route('/location/<uri>')
def location(uri):
    return "foo based on location"

@app.route('/technique/<uri>')
def technique(uri):
    return "fiep based on technique"

