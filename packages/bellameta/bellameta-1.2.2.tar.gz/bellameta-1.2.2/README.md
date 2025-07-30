# Ballatrix Metadata

A microservice managing metadata of whole slide image (WSI) scans for digital pathology applications.

It operates on a storage sqlite database created by the [bellastore](https://github.com/spang-lab/bellastore) package.\
This database is particularly helpful when querying metadata of specific slides for downstream tasks
via our custom digital pathology API `bellapi`.

## Installation

The source code is currently hosted under [https://github.com/spang-lab/bellameta](https://github.com/spang-lab/bellameta).

Binary installers are available at PyPi.

```sh
pip install bellameta
```

## Usage

Under [docs/.env](docs/.env) you find a simple template for an .env file that needs to be located in your current environment and hold
the path to a `yaml` config file. A minimal config file is provided under [docs/bellameta.yaml](docs/bellameta.yaml).
This config defines the valid `Cohort` and `Task` types accesible by the package:

```python
from dotenv import load_dotenv
load_dotenv()

from bellameta.types import Cohort
print(Cohort.list())
```


In order to add metadata to a cohort of scans, a child class of the abstract base class `Metadata` needs to be implemented:

```python
from bellameta.database import Db
from bellameta.types import Cohort, Task
from bellameta.base_metadata import Metadata

class Example(Metadata):
    '''
    An example class inheriting from Metadata.

    We imagine this class to implement the metadata of a new cohort of scans that just arrived from the clinic.
    '''

    def __init__(self, db: Db):
        # here we need to specify the absolute path to the ingress directory as given in the ingress table
        # this serves as the identifier for our cohort
        super().__init__(db, '/tmp/tmpytfd3_47/example_cohort')
    def get_cohort(self, hash):
        # typing for cohorts is provided via bellameta/types
        return Cohort.Example.to_string()
    def get_stain(self, hash):
        # typing for stains is provided via pamly
        return Stain.to_string(Stain('HE'))
    def get_task(self, hash):
        # typing for tasks is provided via bellameta/types
        return [Task.Subtyping.to_string()]
```

In order to write this metadata to the database the class needs to be instantiated:

```python
example = Example(db=db)
example.write_many()
```

## Documentation

Along with the [source code](https://github.com/spang-lab/bellameta), under [docs/demo.ipynb](docs/demo.ipynb), we provide a demo leading you through the features of this package via an application scenario.



