BITBUCKET_REPO_SLUG := "sphinxcontrib"
BITBUCKET_WORKSPACE := "byteb4rb1e"
DIST_PATH_PREFIX := "dist/"
TWINE_USERNAME := "__token__"
GPG_SIGNER_FINGERPRINT := "91CD826E74B0174D181903DEF97C70941CD8C4EF"

.PHONY: chore configure requirements-dev.txt requirements.txt publish archive

all: chore

chore: requirements.txt requirements-dev.txt bitbucket-pipelines.yaml

Pipfile.lock: Pipfile
	python3 -m pipenv lock -v

bitbucket-pipelines.yml: bitbucket-pipelines.yml.m4
	m4 $@.m4 > $@

requirements-dev.txt: Pipfile.lock
	python3 -m pipenv requirements --exclude-markers --dev-only > requirements-dev.txt

requirements.txt: Pipfile.lock
	python3 -m pipenv requirements --exclude-markers > requirements.txt

configure: configure.ac
	autoconf

test-reports/integration:
	python3 -m pipenv run -v test-integration

test-reports/unit:
	python3 -m pipenv run -v test-unit

test-reports/static:
	python3 -m pipenv run -v test-static

build/doc: docs
	python3 -m pipenv run -v doc

dist:
	python3 -m pipenv run -v dist
ifdef SIGN
	for path in $(DIST_PATH_PREFIX)*.tar.gz $(DIST_PATH_PREFIX)*.whl; do \
		echo "$$path"; \
		gpg --detach-sign --local-user $(GPG_SIGNER_FINGERPRINT) -v -a --yes "$$path"; \
	done
endif

publish: dist
ifndef TWINE_PASSWORD
	$(error TWINE_PASSWORD not set)
endif
	for path in $(DIST_PATH_PREFIX)*.tar.gz $(DIST_PATH_PREFIX)*.whl; do \
		echo "$$path"; \
		twine upload $$path $$(test -f "$$path".asc && echo "$$path.asc"); \
	done

archive: dist
ifndef BITBUCKET_ACCESS_TOKEN
	$(error BITBUCKET_ACCESS_TOKEN not set)
endif
	for path in $(DIST_PATH_PREFIX)*; do \
		echo "$$path"; \
		curl \
			--request POST \
			--header "Authorization: Bearer $$BITBUCKET_ACCESS_TOKEN" \
			--form "files=@$$path;filename=$$(basename "$$path")" \
			--fail \
			https://api.bitbucket.org/2.0/repositories/$(BITBUCKET_WORKSPACE)/$(BITBUCKET_REPO_SLUG)/downloads; \
	done

clean:
	rm -rvf autom4te.cache/ config.status config.log configure~ dist/ build/
