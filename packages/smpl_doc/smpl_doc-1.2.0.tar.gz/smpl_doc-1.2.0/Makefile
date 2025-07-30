livehtml:
	hatch run full:$(MAKE) -C docs livehtml

html:
	hatch run full:$(MAKE) -C docs html

doc: html

install:
	hatch env create
	python3 -m pip install --user .

build:
	hatch build

test:
	rm -f .coverage coverage.xml
	hatch test

commit:
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean:
	rm -r docs/build docs/source/_autosummary
	rm -r .eggs .pytest_cache *.egg-info


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
