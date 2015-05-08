SETUP=python setup.py
IDENTITY='Anton Simernia'

test:
	$(SETUP) nosetests

rst:
	pandoc README.md -t rst -o README.rst

clean:
	$(SETUP) clean

flake8:
	$(SETUP) flake8

release: flake8 test rst
	 $(SETUP) sdist upload -r pypi -sign --i $(IDENTITY)
