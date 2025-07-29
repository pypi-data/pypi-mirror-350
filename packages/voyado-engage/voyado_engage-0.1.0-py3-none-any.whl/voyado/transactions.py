"""
Transactions (Receipts) API for Voyado Engage.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from .base import BaseAPIClient


class TransactionsAPI(BaseAPIClient):
    """Handle transaction/receipt-related operations."""
    
    def create_receipt(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new receipt/transaction.
        
        Args:
            receipt_data: Receipt data including items, totals, etc.
            
        Returns:
            Created receipt information
        """
        return self.post('/receipts', data=receipt_data)
    
    def create_return(self, return_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a return transaction.
        
        Args:
            return_data: Return data including items being returned
            
        Returns:
            Created return information
        """
        # Returns use the same endpoint but with negative quantities
        return self.post('/receipts', data=return_data)
    
    def get_by_contact(
        self,
        contact_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        offset: int = 0,
        count: int = 50
    ) -> Dict[str, Any]:
        """
        Get transactions for a specific contact.
        
        Args:
            contact_id: The contact's unique ID
            from_date: Start date for filtering
            to_date: End date for filtering
            offset: Number of items to skip
            count: Number of items to return
            
        Returns:
            Dictionary with transactions and pagination info
        """
        params = {
            'offset': offset,
            'count': min(count, 100)
        }
        
        if from_date:
            params['fromDate'] = from_date.isoformat()
        if to_date:
            params['toDate'] = to_date.isoformat()
            
        return self.get(f'/contacts/{contact_id}/transactions', params=params)
