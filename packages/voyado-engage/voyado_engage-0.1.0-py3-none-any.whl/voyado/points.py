"""
Points API for Voyado Engage.
"""

from typing import Dict, Any, Optional
from .base import BaseAPIClient


class PointsAPI(BaseAPIClient):
    """Handle points-related operations."""
    
    def get_balance(self, contact_id: str) -> Dict[str, Any]:
        """
        Get points balance for a contact.
        
        Args:
            contact_id: The contact's unique ID
            
        Returns:
            Points balance information
        """
        return self.get(f'/contacts/{contact_id}/points')
    
    def add_points(
        self,
        contact_id: str,
        points: int,
        reason: str,
        store_external_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add points to a contact's balance.
        
        Args:
            contact_id: The contact's unique ID
            points: Number of points to add
            reason: Reason for adding points
            store_external_id: External ID of the store
            
        Returns:
            Updated points information
        """
        data = {
            'points': points,
            'reason': reason
        }
        
        if store_external_id:
            data['storeExternalId'] = store_external_id
            
        return self.post(f'/contacts/{contact_id}/points/add', data=data)
    
    def subtract_points(
        self,
        contact_id: str,
        points: int,
        reason: str,
        store_external_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Subtract points from a contact's balance.
        
        Args:
            contact_id: The contact's unique ID
            points: Number of points to subtract
            reason: Reason for subtracting points
            store_external_id: External ID of the store
            
        Returns:
            Updated points information
        """
        data = {
            'points': points,
            'reason': reason
        }
        
        if store_external_id:
            data['storeExternalId'] = store_external_id
            
        return self.post(f'/contacts/{contact_id}/points/subtract', data=data)
    
    def get_transactions(
        self,
        contact_id: str,
        offset: int = 0,
        count: int = 50
    ) -> Dict[str, Any]:
        """
        Get points transaction history for a contact.
        
        Args:
            contact_id: The contact's unique ID
            offset: Number of items to skip
            count: Number of items to return
            
        Returns:
            Points transaction history
        """
        params = {
            'offset': offset,
            'count': min(count, 100)
        }
        
        return self.get(f'/contacts/{contact_id}/points/transactions', params=params)
