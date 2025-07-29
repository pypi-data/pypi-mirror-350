"""
Main Voyado Engage API client.
"""

from typing import Optional
from .base import BaseAPIClient
from .contacts import ContactsAPI
from .orders import OrdersAPI
from .transactions import TransactionsAPI
from .vouchers import VouchersAPI
from .promotions import PromotionsAPI
from .points import PointsAPI


class VoyadoClient:
    """
    Main client for interacting with Voyado Engage API.
    
    Example:
        client = VoyadoClient(
            api_key="your-api-key",
            base_url="https://your-instance.voyado.com",
            user_agent="YourApp/1.0"
        )
        
        # Create a contact
        contact = client.contacts.create({
            "email": "test@example.com",
            "firstName": "John",
            "lastName": "Doe"
        })
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        user_agent: str = "VoyadoPython/0.1.0"
    ):
        """
        Initialize the Voyado client.
        
        Args:
            api_key: Your Voyado API key
            base_url: Base URL for your Voyado instance (e.g., https://yourinstance.voyado.com)
            user_agent: User agent string for API requests
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.user_agent = user_agent
        
        # Initialize API modules
        self.contacts = ContactsAPI(api_key, base_url, user_agent)
        self.orders = OrdersAPI(api_key, base_url, user_agent)
        self.transactions = TransactionsAPI(api_key, base_url, user_agent)
        self.vouchers = VouchersAPI(api_key, base_url, user_agent)
        self.promotions = PromotionsAPI(api_key, base_url, user_agent)
        self.points = PointsAPI(api_key, base_url, user_agent)
    
    def test_connection(self) -> bool:
        """
        Test the API connection by getting contact count.
        
        Returns:
            True if connection is successful
        """
        try:
            count = self.contacts.get_count()
            return isinstance(count, int) and count >= 0
        except Exception:
            return False
