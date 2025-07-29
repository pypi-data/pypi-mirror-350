"""
Promotions API for Voyado Engage.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPIClient


class PromotionsAPI(BaseAPIClient):
    """Handle promotion-related operations."""
    
    def get_by_contact(
        self,
        contact_id: str,
        valid_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get promotions available for a specific contact.
        
        Args:
            contact_id: The contact's unique ID
            valid_only: Only return currently valid promotions
            
        Returns:
            List of available promotions
        """
        params = {}
        if valid_only:
            params['validOnly'] = 'true'
            
        return self.get(f'/contacts/{contact_id}/promotions', params=params)
    
    def assign(
        self,
        contact_id: str,
        promotion_id: str
    ) -> Dict[str, Any]:
        """
        Assign a promotion to a contact.
        
        Args:
            contact_id: The contact's unique ID
            promotion_id: The promotion ID to assign
            
        Returns:
            Assignment result
        """
        return self.post(
            f'/contacts/{contact_id}/promotions/{promotion_id}/assign',
            data={}
        )
    
    def redeem(
        self,
        contact_id: str,
        promotion_id: str,
        store_external_id: Optional[str] = None,
        receipt_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Redeem a promotion for a contact.
        
        Args:
            contact_id: The contact's unique ID
            promotion_id: The promotion ID to redeem
            store_external_id: External ID of the store
            receipt_id: Associated receipt ID
            
        Returns:
            Redemption result
        """
        data = {}
        
        if store_external_id:
            data['storeExternalId'] = store_external_id
        if receipt_id:
            data['receiptId'] = receipt_id
            
        return self.post(
            f'/contacts/{contact_id}/promotions/{promotion_id}/redeem',
            data=data
        )
