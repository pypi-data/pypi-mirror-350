# The official Yield SDK for Python

## Installation

```sh
pip install yield-sdk
```

## Usage

```python
import yield_sdk
import os

# for security, never commit the actual key in your code
client = yield_sdk.SyncClient(os.environ["YIELD_API_KEY"])

# fetch an existing order
order = client.order.fetch("ord_...")
print(order.customer.registered_name)

# or create a new one
new_order = client.order.create(dict(
    customer_id="org_...",
    total_amount="PHP 1234.50",
    note="Test order from the Python SDK!",
))
```
