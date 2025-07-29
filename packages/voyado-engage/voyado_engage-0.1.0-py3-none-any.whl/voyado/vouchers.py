"""
Vouchers API for Voyado Engage.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPIClient


class VouchersAPI(BaseAPIClient):
    """Handle voucher-related operations."""
    
    def get_by_contact(
        self,
        contact_id: str,
        offset: int = 0,
        count: int = 50,
        status_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get vouchers for a specific contact.
        
        Args:
            contact_id: The contact's unique ID
            offset: Number of items to skip
            count: Number of items to return
            status_filter: Filter by status (e.g., 'Active', 'Used', 'Expired')
            
        Returns:
            Dictionary with vouchers and pagination info
        """
        params = {
            'offset': offset,
            'count': min(count, 100)
        }
        
        if status_filter:
            params['statusFilter'] = status_filter
            
        return self.get(f'/contacts/{contact_id}/vouchers', params=params)
    
    def redeem(
        self,
        contact_id: str,
        voucher_code: str,
        store_external_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Redeem a voucher for a contact.
        
        Args:
            contact_id: The contact's unique ID
            voucher_code: The voucher code to redeem
            store_external_id: External ID of the store where redemption occurs
            
        Returns:
            Redemption result
        """
        data = {
            'voucherCode': voucher_code
        }
        
        if store_external_id:
            data['storeExternalId'] = store_external_id
            
        return self.post(f'/contacts/{contact_id}/vouchers/redeem', data=data)
    
    def reactivate(
        self,
        contact_id: str,
        voucher_code: str
    ) -> Dict[str, Any]:
        """
        Reactivate a previously used voucher.
        
        Args:
            contact_id: The contact's unique ID
            voucher_code: The voucher code to reactivate
            
        Returns:
            Reactivation result
        """
        data = {
            'voucherCode': voucher_code
        }
        
        return self.post(f'/contacts/{contact_id}/vouchers/reactivate', data=data)
