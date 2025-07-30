# hume_api

A simple Python client for the Hume API with audio streaming support.

## Installation

```sh
pip install hume_api
```

## Usage

```python
from hume_api import HumeClient

client = HumeClient(
    api_url="wss://hume-8cac.onrender.com",
    access_token=access_token,
    enable_audio=True
)

response = client.responses_create(
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```
