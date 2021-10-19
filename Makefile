include makerules/makerules.mk
include makerules/pipeline.mk
include makerules/datapackage.mk
include makerules/development.mk

DB=dataset/entity.sqlite3

first-pass::
	bin/download.sh
	bin/index.py

second-pass::	$(DB)

$(DB):	bin/load.py
	@rm -f $@
	@mkdir -p dataset/
	python3 bin/load.py $@

datasette:	$(DB)
	datasette serve $(DB)

clean::
	rm -rf ./var

clobber::
	rm -rf dataset/
