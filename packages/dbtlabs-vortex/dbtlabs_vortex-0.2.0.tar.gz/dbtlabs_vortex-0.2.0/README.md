# Vortex Python Client

A Python client for sending data to the Vortex.

## Overview

This client provides an easy way to send properly formatted messages to Kafka topics that will be consumed by the Vortex service and written to Iceberg tables.

The client:
- Accepts arbitrary protobufs onto a buffer via `log_proto`
- Flushes messages in a background thread so that `log_proto` calls do not block

## Installation

### Prerequisites

- Python 3.11, 3.12, 3.13

### Setup

```bash
# From the clients/python directory
uv sync --all-extras
```

## Quick Start

```python
from dbtlabs_vortex.producer import log_proto, shutdown

# Send JSON data
log_proto(... proto ...)

# Wait for all messages to be delivered
shutdown(timeout_seconds=0.500)
```

## Examples

There is one example included in the `examples/` directory. You can run it with:

```bash
uv run examples/send_batch.py
```

This will send some generated events to a locally running Vortex. It also serves as a reference
implementation for how to log events to Vortex using existing protos.

## Error Handling
