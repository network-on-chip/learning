.PHONY: install serve build clean deploy

install:
	pip install -r requirements.txt

serve:
	mkdocs serve

build:
	mkdocs build --strict

clean:
	rm -rf site/
