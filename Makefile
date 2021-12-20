include makerules/makerules.mk
include makerules/pipeline.mk
include makerules/datapackage.mk
include makerules/development.mk

DB=dataset/entity.sqlite3
DB_SUM=dataset/entity.sqlite3.md5sum

first-pass:: $(DB_SUM)

dataset/entity.csv: bin/index.py var/dataset/organisation.csv
	@mkdir -p var/dataset/
	bin/download.sh
	@mkdir -p dataset/
	python3 bin/index.py

dataset/checksum.csv: bin/checksum.sh dataset/entity.csv
	bin/checksum.sh > $@

$(DB):	bin/load.py dataset/entity.csv dataset/checksum.csv
	@mkdir -p dataset/
	python3 bin/load.py $@
	echo 'select count(*) from entity where dataset = "tree";' | sqlite3 $@

$(DB_SUM): $(DB)
	md5sum $(DB) | tee $(DB_SUM)

datasette:
	datasette serve $(DB) \
	--setting sql_time_limit_ms 5000 \
	--load-extension $(SPATIALITE_EXTENSION) \
	--metadata metadata.json

init::
	datasette install datasette-leaflet-geojson
	sqlite3 --version
	-ls -l /usr/lib/x86_64-linux-gnu/*spatialite*

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
