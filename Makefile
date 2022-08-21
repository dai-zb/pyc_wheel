.PHONY: build install uninstall lint clean

project_name =  pyc
python = python
pip = pip

build: clean lint
	# sdist  将源码进行打包
	# python setup.py sdist bdist_wheel
	$(python) setup.py bdist_wheel

build_pyc: build
	# $(python) ./ src $(project_name)
	$(python) ./

install: uninstall build
	$(pip) install dist/*.whl

install_pyc: uninstall build_pyc
	$(pip) install .dist/*.whl

uninstall:
	$(pip) uninstall -y $(project_name)

lint:
	mypy src/$(project_name)

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

	rm -rf build
	rm -rf dist .dist .pyc
	rm -rf src/$(project_name).egg-info

	rm -rf .mypy_cache

