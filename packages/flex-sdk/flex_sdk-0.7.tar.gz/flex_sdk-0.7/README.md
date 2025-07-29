Run this command :

```pip install flex-sdk```

Example usage : 

```
import os
from flex.flex_api_client import FlexApiClient
from flex.flex_objects import Collection, Item

base_url = os.environ['FLEX_ENV_URL'] # for exemple, https://my-env.com/api
username = os.environ['FLEX_ENV_USERNAME']
password = os.environ['FLEX_ENV_PASSWORD']
```

### Parse a CSV of asset IDs and launch a job on each asset
```
from flex.flex_api_client import FlexApiClient
import csv

flex_api_client = FlexApiClient(base_url, username, password)

with open('assets_to_fix.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)

    for row in reader:
        asset_id = row[0]
        job = flex_api_client.create_job({'assetId':asset_id, 'actionId': <actionId>})   
        print(f'Launched job id {job.id} on asset id {asset_id}')
```

### Delete annotations with 00:00:00:00 duration from an asset

```
from flex.flex_api_client import FlexApiClient
from flex.flex_objects import Annotation

flex_api_client = FlexApiClient(base_url, username, password)

asset_id = <assetId>

annotations = flex_api_client.get_annotations(asset_id)

for annotation in annotations:
    if (annotation.timestamp_in == annotation.timestamp_out):
        flex_api_client.delete_annotation(annotation.id)
```

### Deep dive

Find more complex examples in the examples repository, such as [this script](examples/extract_assets_with_wrong_keyframes.py).

Feel free to contribute and add your script examples. Please make sure to **always remove environment related information**.
