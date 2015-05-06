SETUP=python setup.py
IDENTITY='Anton Simernia'

test:
	$(SETUP) test

rst:
	pandoc README.md -t rst -o README.rst

clean:
	$(SETUP) clean

release: test rst
	 $(SETUP) sdist upload -r pypi -sign --i $(IDENTITY)
