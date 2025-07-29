"""
Example: Working with Orders in Voyado Engage
"""

import os
from datetime import datetime, timedelta
from voyado import VoyadoClient

# Initialize client
client = VoyadoClient(
    api_key=os.getenv('VOYADO_API_KEY', 'your-api-key'),
    base_url=os.getenv('VOYADO_BASE_URL', 'https://your-instance.voyado.com')
)

# First, let's find or create a contact
contact_id = None
email = "order.example@test.com"

try:
    # Search for existing contact
    contacts = client.contacts.search(email=email)
    if contacts:
        contact_id = contacts[0]['id']
        print(f"Found existing contact: {contact_id}")
    else:
        # Create new contact
        new_contact = client.contacts.create({
            "email": email,
            "firstName": "Order",
            "lastName": "Example",
            "contactType": "Member",
            "countryCode": "SE"
        })
        contact_id = new_contact['id']
        print(f"Created new contact: {contact_id}")
except Exception as e:
    print(f"Error with contact: {e}")
    exit(1)

# Create an order
order_id = f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
print(f"\nCreating order {order_id}...")

order_data = {
    "orderId": order_id,
    "contactId": contact_id,
    "createdDate": datetime.now().isoformat(),
    "storeExternalId": "WEB-SE",
    "currency": "SEK",
    "paymentMethods": [{
        "type": "Card",
        "description": "Visa ****1234",
        "value": 1299.00
    }],
    "totalGrossPrice": 1299.00,
    "totalTax": 259.80,
    "shippingInfo": {
        "firstName": "Order",
        "lastName": "Example",
        "street": "Example Street 123",
        "city": "Stockholm",
        "zipCode": "111 22",
        "country": "Sweden"
    },
    "items": [
        {
            "sku": "SHIRT-001",
            "productId": "SHIRT-001",
            "variantId": "SHIRT-001-M",
            "quantity": 2,
            "grossPaidPrice": 598.00,
            "taxAmount": 119.60,
            "taxPercent": 25.0,
            "description": "Classic T-Shirt - Medium",
            "articleGroup": "Clothing",
            "articleType": "T-Shirt"
        },
        {
            "sku": "JEANS-001",
            "productId": "JEANS-001",
            "variantId": "JEANS-001-32",
            "quantity": 1,
            "grossPaidPrice": 699.00,
            "taxAmount": 139.80,
            "taxPercent": 25.0,
            "description": "Slim Fit Jeans - Size 32",
            "articleGroup": "Clothing",
            "articleType": "Jeans"
        }
    ]
}

try:
    # Create the order
    response = client.orders.create(order_data)
    job_id = response.get('jobId')
    print(f"Order submitted, job ID: {job_id}")
/order/{order_id}",
                "estimatedDelivery": (datetime.now() + timedelta(days=3)).isoformat()
            }
        )
        print("✓ Order confirmation sent!")
        
    elif final_status['status'] == 'CompletedWithErrors':
        print("⚠ Order created with errors:")
        print(final_status.get('errors', 'Unknown errors'))
    else:
        print(f"✗ Order creation failed: {final_status['status']}")
        
except Exception as e:
    print(f"✗ Error creating order: {e}")

# Get orders for the contact
print(f"\nGetting orders for contact {contact_id}...")
try:
    orders_response = client.orders.get_by_contact(contact_id)
    orders = orders_response.get('orders', [])
    
    print(f"Found {len(orders)} order(s)")
    for order in orders[:5]:  # Show first 5
        print(f"- {order['orderId']}: {order['totalGrossPrice']} {order['currency']} ({order['createdDate']})")
        
except Exception as e:
    print(f"✗ Error getting orders: {e}")

# Example: Update order status with shipping action
print(f"\nSimulating order shipment...")
try:
    # In a real scenario, you would wait for actual shipment
    client.orders.send_action(
        order_id=order_id,
        action="ShipOrder",
        version_tag=order.get('versionTag', ''),
        language="en-US",
        data={
            "trackingNumber": "1234567890",
            "carrier": "PostNord",
            "trackingUrl": "https://tracking.postnord.com/1234567890"
        }
    )
    print("✓ Shipment notification sent!")
except Exception as e:
    print(f"✗ Error sending shipment action: {e}")

print("\n✓ Order example completed!")
