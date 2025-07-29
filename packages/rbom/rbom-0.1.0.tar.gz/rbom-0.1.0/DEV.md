# DEV

### Tooling 
- cli
    - to create a rbom.yaml - interactive
    - to validate rbom
- github action for pre and post validation


### Development

Create a virtual env:
```bash
pyenv virtualenv 3.11 rbom
```

Activate the virtual env:
```bash
pyenv activate rbom
```

Install:
```bash
python -m pip install -e .
```

### Packaging

Generate distirbution:
```bash
python3 -m pip install --upgrade build
python3 -m build
```

Upload build
```bash
python3 -m twine upload --repository testpypi dist/*
```