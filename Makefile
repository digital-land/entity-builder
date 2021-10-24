include makerules/makerules.mk
include makerules/pipeline.mk
include makerules/datapackage.mk
include makerules/development.mk

DB=dataset/entity.sqlite3

first-pass:: $(DB)

dataset/entity.csv: bin/index.py var/dataset/organisation.csv
	bin/download.sh
	@mkdir -p dataset/
	python3 bin/index.py

$(DB):	bin/load.py dataset/entity.csv
	@mkdir -p dataset/
	python3 bin/load.py $@

datasette:	$(DB)
	datasette serve $(DB) \
	--setting sql_time_limit_ms 5000 \
	--load-extension $(SPATIALITE_EXTENSION) \
	--metadata metadata.json

init::
	datasette install datasette-leaflet-geojson

clean::
	rm -rf ./var

clobber::
	rm -rf dataset/

var/dataset/organisation.csv:
	python3 bin/organisation.py > $@
