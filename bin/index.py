#!/usr/bin/env python3

# index entity data

import os
import sys
import csv
import json
import glob
from pathlib import Path
from digital_land.specification import Specification
import geojson
import shapely.wkt


def properties(row, fields):
    return {
        field: row[field]
        for field in row
        if row[field]
        and field
        not in ["geography", "geometry", "organisation", "point", "slug"] + fields
    }


organisations = {}
for row in csv.DictReader(open("var/cache/organisation.csv")):
    organisations[row["organisation"]] = row

specification = Specification()
entity_fields = specification.schema_field["entity"]
geometry_fields = specification.schema_field["geometry"]

e = csv.DictWriter(
    open("dataset/entity.csv", "w", newline=""),
    fieldnames=entity_fields,
    extrasaction="ignore",
)
g = csv.DictWriter(
    open("dataset/geometry.csv", "w", newline=""),
    fieldnames=geometry_fields,
    extrasaction="ignore",
)

e.writeheader()
g.writeheader()

for organisation, row in organisations.items():
    row["entity"] = organisations[row["organisation"]]["entity"]

    row["dataset"] = organisation.split(":")[0]
    row[row["dataset"]] = organisation.split(":")[1]

    del row["organisation"]

    if not row.get("json", ""):
        row["json"] = json.dumps(properties(row, entity_fields))
        if row["json"] == {}:
            del row["json"]

    # responsible organisation will be DLUCH for LAs, GLA for Old Oak Common, companies house for companies, etc
    # row["organisation-entity"] = organisations[row["organisation"]]["entity"]

    # organisation,entity,wikidata,name,website,twitter,statistical-geography,boundary,toid,opendatacommunities,opendatacommunities-area,billing-authority,census-area,local-authority-type,combined-authority,esd-inventories,local-resilience-forum,region,addressbase-custodian,company,wikipedia,start-date,end-date

    if not row.get("wikipedia-url", ""):
        row["wikipedia-url"] = row["wikipedia"]

    if row["wikipedia"] and not row.get("wikipedia-url", ""):
        row["wikipedia-url"] = row["wikipedia"]
        del row["wikipedia"]

    if row["wikidata"] and not row.get("wikidata-item", ""):
        row["wikidata-item"] = row["wikidata"]
        del row["wikidata"]

    e.writerow(row)


for path in glob.glob("var/dataset/*.csv"):
    dataset = Path(path).stem
    for row in csv.DictReader(open(path)):
        if row.get("organisation", ""):
            row["organisation-entity"] = organisations[row["organisation"]]["entity"]

        row.setdefault("dataset", dataset)
        row.setdefault("status", 200)

        if not row.get("reference", ""):
            if row.get("geography", ""):
                row["reference"] = row["geography"].split(":")[1]
            elif row.get(dataset, ""):
                row["reference"] = row[dataset]
                del row[dataset]

        if not row.get("typology", ""):
            row["typology"] = specification.field_typology(row["dataset"])

        if not row.get("json", ""):
            row["json"] = json.dumps(properties(row, entity_fields))
            if row["json"] == {}:
                del row["json"]

        if row.get("geometry", ""):
            wkt = shapely.wkt.loads(row["geometry"])
            row["geojson"] = geojson.Feature(geometry=wkt)
            del row["geojson"]["properties"]

        if not row.get("geojson", ""):
            if row.get("point", ""):
                wkt = shapely.wkt.loads(row["point"])
                row["geojson"] = geojson.Feature(geometry=wkt)
                del row["geojson"]["properties"]

        e.writerow(row)
        g.writerow(row)
