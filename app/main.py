from flask import Flask, request, jsonify, abort
import requests
app = Flask(__name__)

from SPARQLWrapper import SPARQLWrapper2
with open('query-nmvw-year.rq') as q_file:
    query_string_year = q_file.read()

SPARQL_ENDPOINT_NMVW = "https://api.data.netwerkdigitaalerfgoed.nl/datasets/ivo/NMVW/services/NMVW-01/sparql"
SPARQL_ENDPOINT_RIJKS = "https://api.data.netwerkdigitaalerfgoed.nl/datasets/hackalod/RM-PublicDomainImages/services/RM-PublicDomainImages/sparql"

nmvw = SPARQLWrapper2(SPARQL_ENDPOINT_NMVW)
# add a default graph, though that can also be part of the query string
# nmvw.addDefaultGraph("http://www.example.org/graph-selected")

@app.route('/year')
def year():
    uri = request.args.get('uri', '')
    nmvw.setQuery(query_string_year.format(uri))
    try :
        ret = nmvw.query()
    except :
        abort()
    return jsonify(ret.fullResult)
    # return jsonify([binding["item"].value for binding in ret.bindings])

@app.route('/location/<uri>')
def location(uri):
    return "foo based on location"

@app.route('/technique/<uri>')
def technique(uri):
    return "fiep based on technique"

