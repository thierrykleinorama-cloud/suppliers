"""
Suppliers — Data Models
"""
from typing import Optional
from pydantic import BaseModel


class Supplier(BaseModel):
    """A supplier record."""
    id: Optional[str] = None
    company: str
    category: Optional[str] = None
    sex: Optional[str] = None          # 'Mr' or 'Mrs'
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = "Spain"
    vat_number: Optional[str] = None
    payment_terms: Optional[str] = None
    iban: Optional[str] = None
    hotels: Optional[list[str]] = None  # ['MIAOU', 'COIN', 'WOUAF']
    rating: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
