# Ballatrix Split

A microservice creating data splits for deep learning applications in digital pathology.

It operates on a storage sqlite database created by the [bellastore](https://github.com/spang-lab/bellastore) package.\
This database is particularly helpful when querying metadata of specific slides for downstream tasks
via our custom digital pathology API `bellapi`.

## Installation

The source code is currently hosted under [https://github.com/spang-lab/bellasplit](https://github.com/spang-lab/bellasplit).

Binary installers are available at PyPi.

```sh
pip install bellasplit
```

## Usage

Under [docs/.env](docs/.env) you find a simple template for an .env file that needs to be located in your current environment and hold
the path to a `yaml` config file. A minimal config file is provided under [docs/bellameta.yaml](docs/bellameta.yaml).
This config in particular defines the valid `SPLITNAME`s available to this package.

```python
from dotenv import load_dotenv
load_dotenv()

from bellasplit.types import Splitname
print(Splitname.list())
```


In order to fetch data for a new split the `DataSource` interface is to be used, implementing the `get_data` method.

```python
from bellameta import types as t

from bellasplit.database import Db
from bellasplit.base_split import DataSource, Split, SplitWriter

class Subtyping(DataSource):
    def __init__(self,
                 db: Db):
        super().__init__(db = db,
                            task= t.Task.Subtyping)

    
    def get_data(self, **kwargs):
        # here we have room for fetching and modifying the data
        # in this minimal example we simply call the filter method, i.e.,
        # the fetched data results from searching the data that
        # satisfies the conditions specified in **kwargs
        data = self.filter(**kwargs)
        return data
```

In order to fetch the data filters can be defined via `**kwargs`:

```python
db = Db()
source = Subtyping(db=db)

# the conditions to filter for
kwargs = {
    'stain': [t.Stain.HE],
    'class': [t.Subtype.DLBCL, t.Subtype.FL],
    'cohort': [t.Cohort.Example]
}

source_data = source.get_data(**kwargs)
```

In order to create and write the final split the `Split` and `SplitWriter` classes are used:

```python
split = Split(source_data = source_data, splitname = Splitname.from_int(0), test_size = 0.4, val_size=0.2)
writer = SplitWriter(db=db, split=split)
writer.write()
```

## Documentation

Along with the [source code](https://github.com/spang-lab/bellasplit), under [docs/demo.ipynb](docs/demo.ipynb), we provide a demo leading you through the features of this package via an application scenario.
For further documentation see also the test suite.
