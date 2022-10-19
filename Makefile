include makerules/makerules.mk
include makerules/pipeline.mk
include makerules/datapackage.mk
include makerules/development.mk

DB=dataset/entity.sqlite3
DB_SUM=dataset/entity.sqlite3.md5sum

first-pass:: $(DB_SUM)

dataset/entity.csv: bin/index.py var/cache/organisation.csv
	@mkdir -p var/dataset/
	bin/download.sh
	@mkdir -p dataset/
	python3 bin/index.py

dataset/checksum.csv: bin/checksum.sh dataset/entity.csv
	bin/checksum.sh > $@

$(DB):	bin/load.py dataset/entity.csv dataset/checksum.csv
	@mkdir -p dataset/
	python3 bin/load.py $@

$(DB_SUM): $(DB)
	md5sum $(DB) | tee $(DB_SUM)

init::
	datasette install datasette-leaflet-geojson
	sqlite3 --version
	-ls -l /usr/lib/x86_64-linux-gnu/*spatialite*

clean::
	rm -rf ./var

clobber::
	rm -rf dataset/
