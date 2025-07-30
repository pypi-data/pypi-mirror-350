# Azure Function State Storage

A simple key-value storage implementation using Azure Blob Storage as backend.

## Features

- Key-value storage with string values
- Automatic container creation
- Time marker functionality
- Thread-safe operations

## Installation

```bash
pip install az-func-state
```

## Usage

```python
from azfuncstate import AzFuncState

# Initialize with your connection string
conn_str = "YOUR_CONNECTION_STRING"
state = AzFuncState(connection_string=conn_str, container_name="mystate")

# Basic key-value operations
state.set("user:123", "active")
status = state.get("user:123")  # Returns "active"

# Time marker operations
state.set_time_marker("last_updated")
last_update = state.get_time_marker("last_updated")
```

## API Reference

### `AzFuncState(connection_string: str, container_name: str)`
Initialize the state storage.

- `connection_string`: Azure Storage account connection string
- `container_name`: Name of the container to use

### Methods

#### `set(key: str, value: str) -> None`
Store a key-value pair.

#### `get(key: str) -> Optional[str]`
Retrieve a value by key. Returns None if key doesn't exist.

#### `set_time_marker(key: str) -> None`
Store current UTC timestamp under the given key.

#### `get_time_marker(key: str) -> datetime`
Retrieve a stored timestamp. Raises ValueError if key doesn't exist.

## Requirements

- Python 3.12+
- azure-storage-blob package