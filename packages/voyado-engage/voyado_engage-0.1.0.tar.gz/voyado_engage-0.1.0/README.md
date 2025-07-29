# Voyado Engage Python Client

A Python client library for interacting with the Voyado Engage API v3.

## Features

- Full support for Voyado Engage API v3
- Type hints for better IDE support
- Comprehensive error handling
- Support for contacts, orders, transactions, and more
- Async support (coming soon)

## Installation

```bash
pip install voyado-engage
```

## Quick Start

```python
from voyado import VoyadoClient

# Initialize the client
client = VoyadoClient(
    api_key="your-api-key",
    base_url="https://your-instance.voyado.com",
    user_agent="YourApp/1.0"
)

# Create a contact
contact = client.contacts.create({
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "contactType": "Member",
    "countryCode": "SE",
    "preferences": {
        "acceptsEmail": True,
        "acceptsSms": True,
        "acceptsPostal": False
    }
})

# Get contact by ID
contact = client.contacts.get(contact_id="contact-id-here")

# Update contact
client.contacts.update(
    contact_id="contact-id-here",
    data={
        "firstName": "Jane",
        "street": "New Street 123"
    }
)

# Search contacts
results = client.contacts.search(
    email="john.doe@example.com"
)
```

## API Documentation

For full API documentation, please visit [Voyado Developer Documentation](https://developer.voyado.com/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
