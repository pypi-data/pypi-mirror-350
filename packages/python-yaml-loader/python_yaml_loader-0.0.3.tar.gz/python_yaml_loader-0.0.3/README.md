# python-yaml-loader
Python yaml loader

# test
pytest tests/

# test coverage
pytest --cov=config_loader tests/

# build
(pip install build)
python -m build

# distribute
(pip install twine)
twine upload dist/*