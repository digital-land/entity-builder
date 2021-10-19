include makerules/makerules.mk
include makerules/pipeline.mk
include makerules/datapackage.mk

DB=dataset/entity.sqlite3

first-pass::
	bin/download.sh

second-pass::	$(DB)

$(DB):	bin/load.py
	@rm -f $@
	python3 bin/load.py $@

datasette:	$(DB)
	datasette serve $(DB)

clean::
	rm -rf ./var

clobber::
	rm -rf dataset/
