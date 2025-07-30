# PyGARD

PyGARD is Python SDK for the GARD (**G**eo **A**nalysis **R**eady **D**ata) service.

## Installation

```bash
$ pip install pygard
```

## Usage

```python
# Import modules
from pygard.config.gardmeta_config import GardMetaConfig
from pygard.service.gardmeta_client import GardMetaClient
from pygard.model.dto_models import DataInstanceMetaRequest

# Initialize the configuration and client
config = GardMetaConfig()
gard_meta_client = GardMetaClient(config=config)

# Query the GARD service by ID
result = gard_meta_client.query_by_id(did=1)
print(result)

data_instance_meta = gard_meta_client.get_data_instance_meta(
    data_mark=DataInstanceMetaRequest(
        did=result.did,
        _format=result.format
    )
)
print(data_instance_meta)
```
