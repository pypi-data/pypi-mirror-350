# Rocinet

A Python package named rocinet.

## Installation
```bash
pip install rocinet
```

## Usage
```python
from datetime import datetime, timezone
from rocinet import Rocinet

ACCESS_TOKEN = '<fill access token>'
DATASET_STR_CODE = '<fill dataset str code>'

rocinet = Rocinet(ACCESS_TOKEN)

with open('last_timestamp.txt', 'r') as f:
    last_timestamp = datetime.fromisoformat(f.read())
new_last_timestamp = datetime.now(tz=timezone.utc)  

for item in rocinet.get_data_items(DATASET_STR_CODE, content_update_after=last_timestamp, content_update_before=new_last_timestamp):
    print(item.content)

with open('last_timestamp.txt', 'w') as f:
    f.write(new_last_timestamp.isoformat())
```
"""