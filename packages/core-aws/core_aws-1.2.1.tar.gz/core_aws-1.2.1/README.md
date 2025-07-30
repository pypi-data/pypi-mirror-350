# core-aws
_______________________________________________________________________________

This project/library contains common elements related to AWS services...

## Execution Environment

### Install libraries
```shell
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```shell
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```shell
source .venv/bin/activate
```

### Install required libraries.
```shell
pip install .
```

### Optional libraries.
```shell
pip install '.[all]'      # For all...
pip install '.[core-cdc]' # For CDC flows...
pip install '.[tests]'    # For tests execution...
```

### Check tests and coverage...
```shell
python manager.py run-tests
python manager.py run-coverage
```
