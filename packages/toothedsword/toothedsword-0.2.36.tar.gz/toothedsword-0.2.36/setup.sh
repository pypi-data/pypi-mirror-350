rm -rf ./dist/toothedsword-*
python3 setup.py sdist bdist_wheel
twine upload dist/*
