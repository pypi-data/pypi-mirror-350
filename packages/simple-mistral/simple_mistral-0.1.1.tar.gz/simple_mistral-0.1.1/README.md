# simple-mistral
Simple Mistral AI API client

## Your simple async and sync Mistral client
![image info](./pictures/mistral.png)

## Installation

You can install the package using pip:

```bash
pip install simple-mistral
```

Or install directly from the source:

```bash
git clone https://github.com/alaex777/simple-mistral.git
cd simple-mistral
pip install -e .
```

## Requirements

- Python 3.9+
- requests (for sync requests)
- aiohttp (for async requests)

## Usage

```python
from simple_mistral import MistralClient

# Initialize the client
client = MistralClient(api_key="your-api-key")

# Synchronous request
response = client.send_request(
    message="What is Python?"
)

# Asynchronous request
response = await client.send_request_async(
    message="What is Python?"
)
```
