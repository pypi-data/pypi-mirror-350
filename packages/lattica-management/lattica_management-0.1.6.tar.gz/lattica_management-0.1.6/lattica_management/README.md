# Lattica Management

A Python client library for managing Lattica's homomorphic encryption platform at the account and administrative level.

## Overview

The `lattica_management` package provides comprehensive administrative tools to manage Lattica's homomorphic encryption platform. This package enables users to:

1. Manage account settings and information
2. Generate and manage query tokens
3. Control worker sessions for model inference
4. Create, update, and monitor AI models
5. Manage visibility and access to models

This package works in conjunction with the `lattica_query` package, which handles the actual homomorphic encryption and inference process.

## Installation

```bash
pip install lattica-management
```

## Prerequisites

- Python 3.10+
- A valid Lattica account token (JWT)

## Key Components

### LatticaManagement

The main interface for administrative operations on the Lattica platform.

```python
from lattica_management.lattica_management import LatticaManagement

# Initialize with your account token
manager = LatticaManagement("your_account_token_here")
```

## Core Functionality

### Account Management

```python
# Get account credits
credits = manager.get_account_credits()
print(f"Account Credits: {credits}")

# Get account information
account_info = manager.get_account_info()
print(f"Account Info: {account_info}")

# Update account information
manager.update_account_info(
    company_name="Your Company",
    contact_name="Your Name",
    email="your.email@example.com",
    phone_number="+1234567890"
)
```

### Token Management

```python
# Generate a query token for a specific model
query_token = manager.generate_query_token("model_id", "my-token-name")

# List all tokens
tokens = manager.list_tokens(status="ACTIVE")

# Get information about a specific token
token_info = manager.get_token_info("token_jwt")

# Delete a token
manager.delete_token("token_id")

# Update token information
manager.update_token_info(
    token_id="token_id",
    token_name="New Token Name",
    token_note="Token for testing",
    status="ACTIVE"
)
```

### Model Management

```python
# Create a new model
model_id = manager.create_model("My Encryption Model")

# List all models
models = manager.list_models()

# Get information about a specific model
model_info = manager.get_model_info("model_id")

# Update model configuration
manager.update_model(
    model_id="model_id",
    model_name="Updated Model Name",
    description="Model description",
    visibility="PRIVATE",
    auto_restart=True
)

# Control model status
manager.activate_model("model_id")
manager.deactivate_model("model_id")
```

### Worker Management

```python
# Start a worker for a model
worker_status = manager.start_worker("model_id")

# Check worker status
status = manager.get_worker_status("model_id", "worker_session_id")

# Get a list of active workers for a model
active_workers = manager.get_active_workers("model_id")

# List worker sessions
worker_sessions = manager.list_worker_sessions(
    model_id="model_id",
    from_date="2025-01-01"
)

# Stop a worker
manager.stop_worker("model_id", "worker_session_id")
```

### Model Uploads

```python
# Upload a plain model file
manager.upload_plain_model("path/to/model_file.pth", "model_id")
```

## API Documentation

### Account Methods
- `get_account_info()` - Retrieve account details
- `update_account_info(company_name, contact_name, email, phone_number)` - Update account information
- `get_account_credits()` - Check remaining account credits
- `retrieve_payment_transaction()` - Get payment history

### Token Methods
- `generate_query_token(model_id, token_name)` - Generate a new token for a model
- `get_token_info(token_jwt)` - Get token details
- `list_tokens(status, model_id, issue_date)` - List tokens with optional filters
- `update_token_info(token_id, token_name, token_note, status)` - Update token details
- `delete_token(token_id)` - Delete a token
- `assign_token_to_model(token_id, model_id)` - Assign a token to a model
- `unassign_token_from_model(token_id, model_id)` - Unassign a token from a model

### Model Methods
- `create_model(model_name)` - Create a new model
- `get_model_info(model_id)` - Get model details
- `list_models(visibility)` - List models with optional visibility filter
- `update_model(model_id, model_name, description, visibility, auto_restart, input_type, output_type, status)` - Update model configuration
- `activate_model(model_id)` - Activate a model
- `deactivate_model(model_id)` - Deactivate a model
- `update_model_visibility(model_id, visibility)` - Update model visibility
- `upload_plain_model(model_file_path, model_id)` - Upload a model file

### Worker Methods
- `start_worker(model_id)` - Start a worker for a model
- `stop_worker(model_id, worker_session_id)` - Stop a worker
- `get_worker_status(model_id, worker_session_id)` - Check worker status
- `get_active_workers(model_id)` - List active workers for a model
- `list_worker_sessions(model_id, from_date, to_date)` - List worker sessions

## Integration with Lattica Query

The management package works hand-in-hand with the `lattica_query` package:

1. Use `lattica_management` to create models and generate tokens
2. Pass the generated tokens to `lattica_query` for secure, encrypted inference

```python
# Generate a token for a model
token = manager.generate_query_token("model_id")

# Use that token with the query client
from lattica_query.lattica_query_client import QueryClient
query_client = QueryClient(token)
```

## Security Considerations

- Keep your account token secure - it provides administrative access to your Lattica resources
- Use appropriate visibility settings for your models based on your security requirements
- Generate separate tokens for different applications to maintain isolation

## License

Proprietary - © Lattica AI

---

For more information, visit [https://www.lattica.ai](https://www.lattica.ai)