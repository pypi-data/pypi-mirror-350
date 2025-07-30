# XTransactionID

A Python package for generating Twitter's X-Client-Transaction-Id, which is used in X (formerly Twitter) API requests.

## Installation

You can install the package using pip:

```bash
pip install xtransactionid
```

## Usage

```python
import requests
from urllib.parse import urlparse
from xtransactionid.utils import generate_headers, handle_x_migration
from xtransactionid import ClientTransaction

# Initialize a session
session = requests.Session()
session.headers = generate_headers()
response = handle_x_migration(session)

# Example usage
url = "https://x.com/i/api/1.1/jot/client_event.json"
method = "POST"
path = urlparse(url=url).path

# Create transaction ID generator
ct = ClientTransaction(response)

# Generate transaction ID
transaction_id = ct.generate_transaction_id(method=method, path=path)
print(transaction_id)
```

## Features

- Generate X-Client-Transaction-Id for X (Twitter) API requests
- Easy to integrate with existing requests sessions
- Handles all the necessary cryptographic operations

## Requirements

- Python 3.6+
- beautifulsoup4

## License

MIT

## Author

Deep Saha (hiremeasadeveloper@gmail.com)

## GitHub Repository

[Transaction-ID-Generator](https://github.com/OfficialDeepSaha/Transaction-ID-Generator)
