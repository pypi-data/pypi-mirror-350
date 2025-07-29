"""
Contacts API for Voyado Engage.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPIClient


class ContactsAPI(BaseAPIClient):
    """Handle contact-related operations."""
    
    def create(
        self,
        data: Dict[str, Any],
        source: Optional[str] = "API",
        store_external_id: Optional[str] = None,
        create_as_unapproved: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new contact.
        
        Args:
            data: Contact data including required fields like email or mobile
            source: Source of the contact creation
            store_external_id: External ID of the store
            create_as_unapproved: Whether to create contact as unapproved
            
        Returns:
            Created contact data
        """
        params = {
            'source': source,
        }
        if store_external_id:
            params['storeExternalId'] = store_external_id
        if create_as_unapproved:
            params['createAsUnapproved'] = 'true'
            
        return self.post('/contacts', data=data, params=params)
    
    def get(self, contact_id: str) -> Dict[str, Any]:
        """
        Get a contact by ID.
        
        Args:
            contact_id: The contact's unique ID
            
        Returns:
            Contact data
        """
        return self.get(f'/contacts/{contact_id}')

    def update(self, contact_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a contact.
        
        Args:
            contact_id: The contact's unique ID
            data: Fields to update (only send fields you want to change)
            
        Returns:
            Updated contact data
        """
        return self.patch(f'/contacts/{contact_id}', data=data)
    
    def delete(self, contact_id: str) -> None:
        """
        Delete a contact.
        
        Args:
            contact_id: The contact's unique ID
        """
        super().delete(f'/contacts/{contact_id}')
    
    def search(
        self,
        email: Optional[str] = None,
        mobile_phone: Optional[str] = None,
        external_id: Optional[str] = None,
        member_number: Optional[str] = None,
        social_security_number: Optional[str] = None,
        discovery_key: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for contacts by various identifiers.
        
        Args:
            email: Email address
            mobile_phone: Mobile phone number
            external_id: External ID
            member_number: Member number
            social_security_number: Social security number
            discovery_key: Discovery key for Elevate integration
            
        Returns:
            List of matching contacts
        """
        # Build query parameters
        identifiers = []
        if email:
            identifiers.append(f'email:{email}')
        if mobile_phone:
            identifiers.append(f'mobilePhone:{mobile_phone}')
        if external_id:
            identifiers.append(f'externalId:{external_id}')
        if member_number:
            identifiers.append(f'memberNumber:{member_number}')
        if social_security_number:
            identifiers.append(f'socialSecurityNumber:{social_security_number}')
        if discovery_key:
            identifiers.append(f'discoveryKey:{discovery_key}')
        
        if not identifiers:
            raise ValueError("At least one identifier must be provided")
        
        params = {'id': ','.join(identifiers)}
        result = self.get('/contacts/id-lookup', params=params)
        
        # The API returns a dictionary with identifiers as keys
        contacts = []
        for identifier, contact_data in result.items():
            if contact_data:
                contacts.append(contact_data)
        
        return contacts
    
    def update_contact_type(self, contact_id: str, contact_type_id: str) -> Dict[str, Any]:
        """
        Update a contact's type.
        
        Args:
            contact_id: The contact's unique ID
            contact_type_id: The new contact type (e.g., 'Member', 'Contact')
            
        Returns:
            Updated contact data
        """
        return self.post(
            f'/contacts/{contact_id}/updateContactType',
            data={},
            params={'contactTypeId': contact_type_id}
        )
    
    def get_count(self) -> int:
        """
        Get the total number of contacts.
        
        Returns:
            Total contact count
        """
        result = self.get('/contacts/count')
        return result.get('count', 0) if isinstance(result, dict) else result
