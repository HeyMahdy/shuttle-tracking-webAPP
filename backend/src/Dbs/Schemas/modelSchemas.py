import uuid

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum



class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    DRIVER = "driver"


class UserBase(BaseModel):
    """Base user model for common attributes"""
    email: str
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        description="Username must be between 3 and 50 characters"
    )
    role: UserRole
    is_active: bool = True
    is_verified: bool = False
    model_config = {
        'from_attributes': True  # Allows conversion from SQLAlchemy model
    }

class UserCreate(UserBase):
    """Model for user creation, includes password"""
    password: str = Field(
        ..., 
        min_length=8, 
        description="Password must be at least 8 characters long"
    )
    model_config = {
        'from_attributes': True  # Allows conversion from SQLAlchemy model
    }



class UserResponse(UserBase):
    """Model for returning user information (excludes sensitive data)"""
    text : str
    created_at: datetime
    model_config = {
        'from_attributes': True  # Allows conversion from SQLAlchemy model
    }



class UserUpdate(BaseModel):
    """Model for updating user information"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    model_config = {
        'from_attributes': True  # Allows conversion from SQLAlchemy model
    }


class Response(BaseModel):
    """Model for returning responses"""
    text: str
    data : Optional[dict] = None

    model_config = {
        'from_attributes': True  # Allows conversion from SQLAlchemy model
    }

class LoginData(BaseModel):
    email : str
    password : str

class Location(BaseModel):
    driverId : uuid.UUID
    latitude: float
    longitude: float
