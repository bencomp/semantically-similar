from flask import Flask, request, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from SPARQLWrapper import SPARQLWrapper2
with open('query-rijks-year.rq') as q_file:
    query_string_year2 = q_file.read()
with open('query-rijks-location.rq') as q_file:
    query_string_location2 = q_file.read()
with open('query-rijks-technique.rq') as q_file:
    query_string_technique2 = q_file.read()

with open('query-nmvw-year.rq') as q_file:
    query_string_year = q_file.read()
with open('query-nmvw-location.rq') as q_file:
    query_string_location = q_file.read()
with open('query-nmvw-technique.rq') as q_file:
    query_string_technique = q_file.read()

with open('query-nmvw-getyear.rq') as q_file:
    get_year_query = q_file.read()
with open('query-rijks-getyear.rq') as q_file:
    get_year_query2 = q_file.read()

SPARQL_ENDPOINT_NMVW = "https://api.data.netwerkdigitaalerfgoed.nl/datasets/ivo/NMVW/services/NMVW-01/sparql"
SPARQL_ENDPOINT_RIJKS = "https://api.data.netwerkdigitaalerfgoed.nl/datasets/hackalod/RM-PublicDomainImages/services/RM-PublicDomainImages/sparql"

nmvw = SPARQLWrapper2(SPARQL_ENDPOINT_NMVW)
rijks = SPARQLWrapper2(SPARQL_ENDPOINT_RIJKS)

@app.route('/year')
def year():
    uri = request.args.get('uri', '')
    year = get_year(uri)
    app.logger.debug("year: {}".format( year))
    if year == []:
        year = "1900"
    app.logger.debug("querying NMVW for year")
    nmvw.setQuery(query_string_year.format(uri, year))
    app.logger.debug("querying Rijks for year")
    rijks.setQuery(query_string_year2.format(uri, year))
    try :
        app.logger.debug("querying NMVW for items")
        ret = nmvw.query()
        app.logger.debug("querying Rijks for items")
        ret2 = rijks.query()
    except Exception as e:
        return "Uh oh", 500
    return linked_art_it(uri, ret.bindings + ret2.bindings)


@app.route('/location')
def location():
    uri = request.args.get('uri', '')
    nmvw.setQuery(query_string_location.format(uri))
    rijks.setQuery(query_string_location2.format(uri))
    try :
        ret = nmvw.query()
        ret2 = rijks.query()
    except :
        abort(404)
    return linked_art_it(uri, ret.bindings + ret2.bindings)

@app.route('/technique')
def technique():
    uri = request.args.get('uri', '')
    nmvw.setQuery(query_string_technique.format(uri))
    rijks.setQuery(query_string_technique2.format(uri))
    try :
        ret = nmvw.query()
        ret2 = rijks.query()
    except :
        abort(404)
    return linked_art_it(uri, ret.bindings + ret2.bindings)

def get_year(uri):
    if "20.500.11840" in uri:
        nmvw.setQuery(get_year_query.format(uri))
        return nmvw.query().getValues("year")
    else:
        rijks.setQuery(get_year_query2.format(uri))
        return rijks.query().getValues("year")


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

