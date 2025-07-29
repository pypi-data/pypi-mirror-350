"""
Utility functions for Voyado Engage client.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import re


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_mobile_phone(phone: str) -> bool:
    """
    Validate mobile phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it starts with + and contains only digits
    return bool(re.match(r'^\+?\d{8,15}$', cleaned))


def format_date_for_api(date: datetime) -> str:
    """
    Format datetime object for Voyado API.
    
    Args:
        date: Datetime object
        
    Returns:
        ISO formatted date string
    """
    return date.isoformat()


def clean_contact_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and validate contact data before sending to API.
    
    Args:
        data: Contact data dictionary
        
    Returns:
        Cleaned contact data
    """
    cleaned = {}
    
    # Only include non-empty values
    for key, value in data.items():
        if value is not None and value != "":
            cleaned[key] = value
    
    # Validate email if present
    if 'email' in cleaned and not validate_email(cleaned['email']):
        raise ValueError(f"Invalid email format: {cleaned['email']}")
    
    # Validate mobile phone if present
    if 'mobilePhone' in cleaned and not validate_mobile_phone(cleaned['mobilePhone']):
        raise ValueError(f"Invalid mobile phone format: {cleaned['mobilePhone']}")
    
    return cleaned


def calculate_tax(gross_price: float, tax_percent: float) -> Dict[str, float]:
    """
    Calculate tax amount from gross price and tax percentage.
    
    Args:
        gross_price: Total price including tax
        tax_percent: Tax percentage (e.g., 25 for 25%)
        
    Returns:
        Dictionary with net_price and tax_amount
    """
    tax_multiplier = tax_percent / 100
    net_price = gross_price / (1 + tax_multiplier)
    tax_amount = gross_price - net_price
    
    return {
        'net_price': round(net_price, 2),
        'tax_amount': round(tax_amount, 2),
        'gross_price': gross_price
    }
