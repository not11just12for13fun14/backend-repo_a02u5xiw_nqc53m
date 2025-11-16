"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

# --- QED Express Schemas ---

class Booking(BaseModel):
    """Bookings for QED Express Trivia events
    Collection name: "booking"
    """
    date: str = Field(..., description="Event date in YYYY-MM-DD")
    start_time: str = Field(..., description="Start time in HH:MM format")
    location: str = Field(..., description="WeWork building/location")
    expected_attendance: Optional[int] = Field(None, ge=0)
    languages: List[str] = Field(default_factory=list, description="Languages for the event")
    format: Literal["Standard", "Themed"] = Field("Standard")
    request_trophy_pack: bool = Field(False, description="If true, will follow up for 10+ trophy pack")
    notes: Optional[str] = Field(None)
    contact_name: Optional[str] = Field(None, description="Community Associate name")
    contact_email: Optional[EmailStr] = Field(None, description="Community Associate email")

class TrophyOrder(BaseModel):
    """Orders for Owl Trophies packs
    Collection name: "trophyorder"
    """
    quantity: int = Field(..., ge=10, description="Minimum order 10 units")
    delivery_address: str = Field(..., description="Full delivery address")
    contact_name: Optional[str] = Field(None)
    contact_email: Optional[EmailStr] = Field(None)
    add_to_invoice: bool = Field(True, description="If true, add to existing invoice; else separate charge")

# Example schemas (kept for reference; not used by this app)
class User(BaseModel):
    name: str
    email: EmailStr
    address: str
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
