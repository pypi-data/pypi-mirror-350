# Edge Addons API

[![CI](https://github.com/web-scrobbler/python-edge-addons-api/actions/workflows/main.yml/badge.svg)](https://github.com/web-scrobbler/python-edge-addons-api/actions/workflows/main.yml)

An API client for publishing addons to the Edge store.

Based on the [PlasmHQ Edge Addons API](https://github.com/PlasmoHQ/edge-addons-api).

## Usage

Obtain the required options for your project. These can be obtained by following the [Microsoft Edge Add-Ons API guide](https://learn.microsoft.com/en-us/microsoft-edge/extensions-chromium/publish/api/using-addons-api).

Once obtained you can submit you addon like below:


```python
from edge_addons_api.client import Options, Client

options = Options(
    product_id="Your product ID",
    client_id="Your client ID",
    api_key="Your API key",
    retry_count=5 # Retry attempts, default 5
    sleep_seconds=3 # Sleep seconds between retries, default 3

)

client = Client(options)

# Upload extension
operation_id = client.submit(
    file_path="/path/to/extension.zip",
    notes="Your upload notes"
)

# Check publish status
client.fetch_publish_status(operation_id)
```

## License

MIT
