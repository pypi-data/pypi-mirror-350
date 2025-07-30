# DEV

### Tooling 
- rbom.yaml file format validator
    - policies
        - id
        - ...
    - name
    - etc..
    - is valid yaml
- cli
    - to create a rbom.yaml - interactive
    - to validate rbom
- github action for pre and post validation

The github action needs to be able to set these values: 
'''
These values must be set in metadata:
Not required means they are set in the RBOM file, but dont have to be auto set.


    - release_id: "release-2025-05-23"
    - timestamp: "2025-05-23T12:00:00Z"
    - commit: "abc123def456gh7890ijklmnopqrs"
    - actor: "ghost-1234567890"
    - notes: "Initial deployment of payment API version 1.0"
    - distribution: 
        - version: "1.0"
        - target: "https://pypi.org/project/rbom/" (not required)
        - channel: "PyPi" (not required)
    

    At a later stage: 
    - sbom:
        format: "cyclonedx-json"
        version: "1.4"
        source: "./sbom.json"
        sha256: "abc123def456gh7890ijklmnopqrs" # replace with actual SHA256 of the SBOM file
        createdAt: "2025-05-23T12:00:00Z" # replace with actual creation timestamp
        createdBy: "Github Actions - SBOM Generator" # replace with actual creator
        supplier: "Acme, Inc" # replace with actual supplier name
'''


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

Upload build TestPyPi
```bash
python3 -m twine upload --repository testpypi dist/*
```


Upload build PyPi
```bash
python3 -m twine upload dist/*
```