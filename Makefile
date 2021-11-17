include makerules/makerules.mk
include makerules/pipeline.mk
include makerules/datapackage.mk
include makerules/development.mk

DB=dataset/entity.sqlite3

first-pass:: $(DB)

dataset/entity.csv: bin/index.py var/dataset/organisation.csv
	@mkdir -p var/dataset/
	bin/download.sh
	@mkdir -p dataset/
	python3 bin/index.py

$(DB):	bin/load.py dataset/entity.csv
	@mkdir -p dataset/
	python3 bin/load.py $@

datasette:
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

var/dataset/organisation.csv: bin/organisation.py
	@mkdir -p var/dataset/
	python3 bin/organisation.py > $@

aws-build::
	aws batch submit-job --job-name entity-db-$(shell date '+%Y-%m-%d-%H-%M-%S') --job-queue dl-batch-queue --job-definition dl-batch-def --container-overrides '{"environment": [{"name":"BATCH_FILE_URL","value":"https://raw.githubusercontent.com/digital-land/docker-builds/main/builder_run.sh"}, {"name" : "REPOSITORY","value" : "entity-builder"}]}'

push::
	aws s3 sync dataset s3://digital-land-collection
