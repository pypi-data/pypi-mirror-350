"""
Orders API for Voyado Engage.
"""

from typing import Dict, Any, Optional, List
import time
from .base import BaseAPIClient


class OrdersAPI(BaseAPIClient):
    """Handle order-related operations."""
    
    def create(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            order_data: Order data including orderId, contactId, items, etc.
            
        Returns:
            Job status information
        """
        return self.post('/orders', data=order_data)
    
    def get(self, order_id: str) -> Dict[str, Any]:
        """
        Get an order by ID.
        
        Args:
            order_id: The order's unique ID
            
        Returns:
            Order data
        """
        return self.get(f'/orders/{order_id}')
    
    def update(self, order_id: str, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing order.
        
        Args:
            order_id: The order's unique ID
            order_data: Updated order data
            
        Returns:
            Job status information
        """
        return self.post(f'/orders/{order_id}', data=order_data)
    
    def delete(self, order_id: str) -> None:
        """
        Delete an order.
        
        Args:
            order_id: The order's unique ID
        """
        super().delete(f'/orders/{order_id}')
    
    def get_by_contact(
        self,
        contact_id: str,
        offset: int = 0,
        count: int = 50
    ) -> Dict[str, Any]:
        """
        Get orders for a specific contact.
        
        Args:
            contact_id: The contact's unique ID
            offset: Number of items to skip
            count: Number of items to return (max 100)
            
        Returns:
            Dictionary with orders and pagination info
        """
        params = {
            'offset': offset,
            'count': min(count, 100)
        }
        return self.get(f'/contacts/{contact_id}/orders', params=params)
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of an order processing job.
        
        Args:
            job_id: The job ID returned from create/update operations
            
        Returns:
            Job status information
        """
        return self.get(f'/orders/jobs/{job_id}')
    
    def wait_for_job(self, job_id: str, timeout: int = 30, poll_interval: int = 1) -> Dict[str, Any]:
        """
        Wait for an order job to complete.
        
        Args:
            job_id: The job ID to monitor
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
            
        Returns:
            Final job status
            
        Raises:
            TimeoutError: If job doesn't complete within timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            
            if status.get('status') in ['Completed', 'CompletedWithErrors', 'Failed']:
                return status
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
    
    def send_action(
        self,
        order_id: str,
        action: str,
        version_tag: str,
        language: str = "en-US",
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Send an action for an order (e.g., to trigger automations).
        
        Args:
            order_id: The order's unique ID
            action: Action name (e.g., 'ConfirmOrder', 'ShipOrder')
            version_tag: Order version tag for consistency
            language: Language code for the action
            data: Additional custom data for the action
        """
        payload = {
            "action": action,
            "versionTag": version_tag,
            "language": language
        }
        if data:
            payload["data"] = data
            
        self.post(f'/orders/{order_id}/action', data=payload)
