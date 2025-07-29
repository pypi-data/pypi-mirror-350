# Bugzee Error Monitoring Client

A client library for Bugzee Error Monitoring service. This library provides error monitoring capabilities for Django and Odoo applications.

## Installation

```bash
pip install bugzee-client
```

## Usage for Django

Add the following to your Django settings:

```python
BUGZEE_PUBLIC_KEY = 'your-project-key'
BUGZEE_API_URL = 'https://bugzee.pro/errors/api/store/'
BUGZEE_ENVIRONMENT = 'production'  # Or 'development', 'staging', etc.

MIDDLEWARE = [
    # ... other middleware
    'bugzee_django.install_middleware',
    # ... other middleware
]
```

## Usage for Odoo

Initialize the client in your Odoo module:

```python
from bugzee_odoo import initialize

initialize(
    public_key='your-project-key',
    api_url='https://bugzee.pro/errors/api/store/',
    environment='production'  # Or 'development', 'staging', etc.
)
```

## Manual Exception Capture

```python
from bugzee_django import capture_exception  # For Django
# or
from bugzee_odoo import capture_exception  # For Odoo

try:
    # Your code here
except Exception as e:
    capture_exception() 