# fastapi-base
how to release module
1. install relational modules
```
pip install setuptools wheel twine
```
2. modify setup.py(optional)
3. build env && upload to pypi
```
python setup.py sdist bdist_wheel
twine upload dist/*
```