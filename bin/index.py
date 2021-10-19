#!/usr/bin/env python3

# index entity data

import os
import sys
import csv
import json
import glob
from pathlib import Path
from digital_land.specification import Specification

csv.field_size_limit(10000000)

organisation = {}
for row in csv.DictReader(open("var/cache/organisation.csv")):
    organisation[row["organisation"]] = row

specification = Specification()
entity_fields = specification.schema_field["entity"]

e = csv.DictWriter(open("dataset/entity.csv", "w", newline=""), fieldnames=entity_fields, extrasaction='ignore')
e.writeheader()

for path in glob.glob('var/dataset/*.csv'):
    dataset = Path(path).stem
    for row in csv.DictReader(open(path)):
        if row.get("organisation", ""):
            row["organisation-entity"] = organisation[row["organisation"]]["entity"]

        row.setdefault("dataset", dataset)
        row.setdefault("status", 200)

        if not row.get("reference", ""):
            if row.get("geography", ""):
                row["reference"] = row["geography"].split(":")[1]

        if "json" not in row:
            o = {field: row[field] for field in row if row[field] and field not in ["geography", "geometry", "organisation", "point", "slug"] + entity_fields}
            if o != {}:
                row["json"] = json.dumps(o)

        e.writerow(row)
