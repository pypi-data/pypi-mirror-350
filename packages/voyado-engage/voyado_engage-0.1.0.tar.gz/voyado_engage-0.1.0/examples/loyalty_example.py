"""
Example: Loyalty Features (Points, Vouchers, Promotions)
"""

import os
from datetime import datetime
from voyado import VoyadoClient

# Initialize client
client = VoyadoClient(
    api_key=os.getenv('VOYADO_API_KEY', 'your-api-key'),
    base_url=os.getenv('VOYADO_BASE_URL', 'https://your-instance.voyado.com')
)

# First, find or create a contact
contact_id = None
email = "loyalty.example@test.com"

try:
    contacts = client.contacts.search(email=email)
    if contacts:
        contact_id = contacts[0]['id']
        print(f"Using existing contact: {contact_id}")
    else:
        new_contact = client.contacts.create({
            "email": email,
            "firstName": "Loyalty",
            "lastName": "Example",
            "contactType": "Member",
            "countryCode": "SE",
            "preferences": {
                "acceptsEmail": True,
                "acceptsSms": True
            }
        })
        contact_id = new_contact['id']
        print(f"Created new contact: {contact_id}")
except Exception as e:
    print(f"Error with contact: {e}")
    exit(1)

# POINTS MANAGEMENT
print("\n=== POINTS MANAGEMENT ===")

# Get current points balance
try:
    points_info = client.points.get_balance(contact_id)
    print(f"Current points balance: {points_info.get('balance', 0)}")
    print(f"Pending points: {points_info.get('pendingPoints', 0)}")
except Exception as e:
    print(f"Error getting points: {e}")

# Add points
try:
    print("\nAdding 100 bonus points...")
    result = client.points.add_points(
        contact_id=contact_id,
        points=100,
        reason="Welcome bonus",
        store_external_id="WEB"
    )
    print(f"✓ Points added! New balance: {result.get('balance', 'Unknown')}")
except Exception as e:
    print(f"✗ Error adding points: {e}")

# Get points transaction history
try:
    print("\nRecent points transactions:")
    transactions = client.points.get_transactions(contact_id, count=5)
    for trans in transactions.get('transactions', [])[:5]:
        print(f"- {trans.get('date')}: {trans.get('points', 0)} points - {trans.get('reason', 'No reason')}")
except Exception as e:
    print(f"Error getting transactions: {e}")

# VOUCHERS
print("\n=== VOUCHERS ===")

# Get available vouchers
try:
    vouchers = client.vouchers.get_by_contact(contact_id, status_filter="Active")
    print(f"Active vouchers: {len(vouchers.get('vouchers', []))}")
    
    for voucher in vouchers.get('vouchers', [])[:3]:
        print(f"- {voucher.get('voucherCode')}: {voucher.get('description', 'No description')}")
        print(f"  Valid until: {voucher.get('validTo', 'No expiry')}")
        print(f"  Value: {voucher.get('value', 0)} {voucher.get('currency', '')}")
except Exception as e:
    print(f"Error getting vouchers: {e}")

# PROMOTIONS
print("\n=== PROMOTIONS ===")

# Get available promotions
try:
    promotions = client.promotions.get_by_contact(contact_id, valid_only=True)
    print(f"Available promotions: {len(promotions)}")
    
    for promo in promotions[:3]:
        print(f"\n- {promo.get('name', 'Unnamed promotion')}")
        print(f"  Description: {promo.get('description', 'No description')}")
        print(f"  Type: {promo.get('type', 'Unknown')}")
        print(f"  Valid: {promo.get('validFrom', 'N/A')} to {promo.get('validTo', 'N/A')}")
        
        # Assign a promotion if available
        if promotions and not promo.get('assigned'):
            try:
                print(f"\n  Assigning promotion '{promo.get('name')}'...")
                client.promotions.assign(
                    contact_id=contact_id,
                    promotion_id=promo['id']
                )
                print("  ✓ Promotion assigned!")
            except Exception as e:
                print(f"  ✗ Error assigning promotion: {e}")
            break
            
except Exception as e:
    print(f"Error with promotions: {e}")

# CREATING A TRANSACTION WITH LOYALTY FEATURES
print("\n=== CREATING TRANSACTION WITH LOYALTY ===")

try:
    receipt_data = {
        "receiptNumber": f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "createdDate": datetime.now().isoformat(),
        "storeExternalId": "STORE-001",
        "currency": "SEK",
        "contact": {
            "matchKey": contact_id,
            "matchKeyType": "ContactId"
        },
        "items": [
            {
                "sku": "LOYALTY-ITEM-001",
                "quantity": 1,
                "grossPaidPrice": 299.00,
                "taxAmount": 59.80,
                "taxPercent": 25.0,
                "description": "Loyalty Test Item"
            }
        ],
        "totalGrossPrice": 299.00,
        "totalTax": 59.80
    }
    
    print("Creating transaction to earn points...")
    result = client.transactions.create_receipt(receipt_data)
    print(f"✓ Transaction created! Points should be awarded based on your loyalty rules.")
    
    # Check updated points balance
    points_info = client.points.get_balance(contact_id)
    print(f"Updated points balance: {points_info.get('balance', 0)}")
    
except Exception as e:
    print(f"✗ Error creating transaction: {e}")

print("\n✓ Loyalty example completed!")
