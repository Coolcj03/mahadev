from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Base schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    images: List[str] = []
    
    class Config:
        from_attributes = True

# Part schemas
class PartBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: int = 0
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None

class PartCreate(PartBase):
    pass

class PartUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None

class PartResponse(PartBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Technician schemas
class TechnicianBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    specialization: Optional[str] = None
    experience_years: int = 0
    is_available: bool = True

class TechnicianCreate(TechnicianBase):
    pass

class TechnicianUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    is_available: Optional[bool] = None

class TechnicianResponse(TechnicianBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Booking schemas
class BookingBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[EmailStr] = None
    service_type: str
    description: Optional[str] = None
    preferred_date: Optional[datetime] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    service_type: Optional[str] = None
    description: Optional[str] = None
    preferred_date: Optional[datetime] = None
    status: Optional[str] = None
    technician_id: Optional[int] = None

class BookingResponse(BookingBase):
    id: int
    status: str
    technician_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    technician: Optional[TechnicianResponse] = None
    
    class Config:
        from_attributes = True

# Feedback schemas
class FeedbackBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    subject: str
    message: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    admin_reply: Optional[str] = None
    is_resolved: Optional[bool] = None

class FeedbackResponse(FeedbackBase):
    id: int
    admin_reply: Optional[str] = None
    is_resolved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Authentication schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Admin user schemas
class AdminUserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class AdminUserCreate(AdminUserBase):
    password: str

class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class AdminUserResponse(AdminUserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
