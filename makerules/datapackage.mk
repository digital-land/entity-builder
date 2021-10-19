ifeq (,$(wildcard ./makerules/specification.mk))
# update local copies of specification files
specification::
	@mkdir -p specification/
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/datapackage.csv' > specification/datapackage.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/datapackage-dataset.csv' > specification/datapackage-dataset.csv
endif
