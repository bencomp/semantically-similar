# Semantically Similar

Semantically Similar is an
API that retrieves a similar item for a given item from
the collections of the [Rijksmuseum Amsterdam][rijks] and
[Nederlandse Museums of World Cultures][nmvw], using SPARQL
to query the collection data.

This API was developed during
[HackaLOD 2019][hack2019] for [Niet te Vergeten][ntv], by
[team ExpLOD][explod].

## Installation

The API is built as a Flask app and is containerised with
Docker.
This repository is set up to automatically trigger builds on
Docker Hub, so that installation can be done by:

<kbd>[sudo] docker pull bencomp/semantically-similar</kbd>

Port 80 is exposed, so you would probably want to map it
when starting a container, for example to port 2345:

<kbd>[sudo] docker run --name lod_api -p 2345:80 bencomp/semantically-similar</kbd>

## Usage

The API has three similar endpoints, to find items in both
museums' collections that share some aspect. *(To call all
returned items semantically similar is not necessarily correct.)*

The URI of the input must be provided in the `uri` query parameter.

All endpoints return [JSON-LD] responses following a very small part
of the [Linked Art][linkedart] data model.

### Find items from the same year

The `/year` endpoint is currently the only working endpoint.
It tries to find the year of the creation date and uses that to query
for other items from that year.

```
GET http://[server]/year?uri=<uri>
```

### Find items from the same location of origin

**The `/location` endpoint is currently not working correctly.**
It tries to find the item's location of creation and uses that to query
for other items from that location.

```
GET http://[server]/location?uri=<uri>
```

### Find items created with the same techniques

**The `/technique` endpoint is currently not working correctly.**
It tries to find the item's means of creation and uses that to query
for other items created with the same technique.

```
GET http://[server]/technique?uri=<uri>
```


## License

GPLv3, or later.

[rijks]: https://www.rijksmuseum.nl/
[nmvw]: http://museumovermensen.nl/
[hack2019]: https://hackalod.com/
[ntv]: https://hackalod.com/index.php/2019/12/24/teams-en-resultaten-2019/
[explod]: https://hackalod.com/index.php/2019/12/24/teams-en-resultaten-2019/
[JSON-LD]: https://json-ld.org/
[linkedart]: https://linked.art/