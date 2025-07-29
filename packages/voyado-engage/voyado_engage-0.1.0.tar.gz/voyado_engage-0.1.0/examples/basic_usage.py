"""
Example usage of the Voyado Engage Python client.
"""

import os
from datetime import datetime
from voyado import VoyadoClient

# Initialize the client
# You can set these as environment variables for security
API_KEY = os.getenv('VOYADO_API_KEY', 'your-api-key-here')
BASE_URL = os.getenv('VOYADO_BASE_URL', 'https://your-instance.voyado.com')

client = VoyadoClient(
    api_key=API_KEY,
    base_url=BASE_URL,
    user_agent="VoyadoExample/1.0"
)

# Test connection
print("Testing connection...")
if client.test_connection():
    print("✓ Connection successful!")
else:
    print("✗ Connection failed. Check your API key and base URL.")
    exit(1)

# Example 1: Create a contact
print("\n1. Creating a contact...")
try:
    new_contact = client.contacts.create({
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "mobilePhone": "+46701234567",
        "countryCode": "SE",
        "birthDay": "1990-01-15",
        "contactType": "Member",
        "preferences": {
            "acceptsEmail": True,
            "acceptsSms": True,
            "acceptsPostal": False
        },
        "consents": [{
            "id": "memberConsent",
            "value": True,
            "date": datetime.now().isoformat(),
            "source": "API",
            "comment": "Accepted terms via API"
        }]
    })
    print(f"✓ Contact created with ID: {new_contact['id']}")
    contact_id = new_contact['id']
except Exception as e:
    print(f"✗ Failed to create contact: {e}")
    contact_id = None

# Example 2: Search for contacts
print("\n2. Searching for contacts...")
try:
    search_results = client.contacts.search(email="john.doe@example.com")
    print(f"✓ Found {len(search_results)} contact(s)")
    if search_results and not contact_id:
        contact_id = search_results[0]['id']
except Exception as e:
    print(f"✗ Search failed: {e}")

# Example 3: Update a contact
if contact_id:
    print("\n3. Updating contact...")
    try:
        updated_contact = client.contacts.update(
            contact_id=contact_id,
            data={
                "street": "New Street 123",
                "city": "Stockholm"
            }
        )
        print("✓ Contact updated successfully")
    except Exception as e:
        print(f"✗ Update failed: {e}")

# Example 4: Create an order
if contact_id:
    print("\n4. Creating an order...")
    try:
        order_data = {
            "orderId": f"ORDER-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "contactId": contact_id,
            "createdDate": datetime.now().isoformat(),
            "storeExternalId": "STORE-001",
            "currency": "SEK",
            "totalGrossPrice": 499.00,
            "items": [{
                "sku": "PROD-001",
                "quantity": 1,
                "grossPaidPrice": 499.00,
                "description": "Example Product"
            }]
        }
        
        order_response = client.orders.create(order_data)
        print(f"✓ Order created, job ID: {order_response.get('jobId')}")
        
        # Wait for order processing
        if order_response.get('jobId'):
            print("  Waiting for order processing...")
            final_status = client.orders.wait_for_job(
                job_id=order_response['jobId'],
                timeout=10
            )
            print(f"  Order status: {final_status.get('status')}")
    except Exception as e:
        print(f"✗ Order creation failed: {e}")

# Example 5: Get contact's points balance
if contact_id:
    print("\n5. Getting points balance...")
    try:
        points = client.points.get_balance(contact_id)
        print(f"✓ Points balance: {points.get('balance', 0)}")
    except Exception as e:
        print(f"✗ Failed to get points: {e}")

# Example 6: Get available promotions
if contact_id:
    print("\n6. Getting available promotions...")
    try:
        promotions = client.promotions.get_by_contact(contact_id)
        print(f"✓ Found {len(promotions)} promotion(s)")
        for promo in promotions[:3]:  # Show first 3
            print(f"  - {promo.get('name', 'Unnamed promotion')}")
    except Exception as e:
        print(f"✗ Failed to get promotions: {e}")

print("\n✓ Example completed!")
