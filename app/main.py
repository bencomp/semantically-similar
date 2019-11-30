from flask import Flask, request, jsonify, abort

app = Flask(__name__)

from SPARQLWrapper import SPARQLWrapper2
with open('query-nmvw-year.rq') as q_file:
    query_string_year = q_file.read()

with open('query-nmvw-year.rq') as q_file:
    query_string_year = q_file.read()
with open('query-nmvw-location.rq') as q_file:
    query_string_location = q_file.read()
with open('query-nmvw-technique.rq') as q_file:
    query_string_technique = q_file.read()
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
    return linked_art_it(uri, ret.bindings)
    # return jsonify([binding["item"].value for binding in ret.bindings])

@app.route('/location')
def location():
    uri = request.args.get('uri', '')
    nmvw.setQuery(query_string_location.format(uri))
    try :
        ret = nmvw.query()
    except :
        abort()
    return linked_art_it(uri, ret.bindings)

@app.route('/technique')
def technique():
    uri = request.args.get('uri', '')
    nmvw.setQuery(query_string_technique.format(uri))
    try :
        ret = nmvw.query()
    except :
        abort()
    return linked_art_it(uri, ret.bindings)

def linked_art_it(uri, bindings):
    """Produce Linked Art"""
    return jsonify([ 
    {
        "@context": "https://linked.art/ns/v1/linked-art.json",
        "id": binding["item"].value,
        "representation": [
        {
            "_label": "NDE LOD",
            "id": binding["img"].value,
            "type": "VisualItem"
        }
        ],
        "type": "HumanMadeObject"
    } for binding in bindings])

