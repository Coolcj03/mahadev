from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Product, ProductImage, Part, Technician, Booking, Feedback, AdminUser
from schemas import *
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password utilities
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT utilities
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authentication
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(AdminUser).filter(AdminUser.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Product CRUD operations
def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_new_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_existing_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_existing_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# Part CRUD operations
def get_all_parts(db: Session):
    return db.query(Part).all()

def get_part_by_id(db: Session, part_id: int):
    return db.query(Part).filter(Part.id == part_id).first()

def create_new_part(db: Session, part: PartCreate):
    db_part = Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def update_existing_part(db: Session, part_id: int, part: PartUpdate):
    db_part = db.query(Part).filter(Part.id == part_id).first()
    if db_part:
        update_data = part.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_part, field, value)
        db.commit()
        db.refresh(db_part)
    return db_part

def delete_existing_part(db: Session, part_id: int):
    db_part = db.query(Part).filter(Part.id == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
        return True
    return False

# Technician CRUD operations
def get_all_technicians(db: Session):
    return db.query(Technician).all()

def get_technician_by_id(db: Session, technician_id: int):
    return db.query(Technician).filter(Technician.id == technician_id).first()

def create_new_technician(db: Session, technician: TechnicianCreate):
    db_technician = Technician(**technician.dict())
    db.add(db_technician)
    db.commit()
    db.refresh(db_technician)
    return db_technician

def update_existing_technician(db: Session, technician_id: int, technician: TechnicianUpdate):
    db_technician = db.query(Technician).filter(Technician.id == technician_id).first()
    if db_technician:
        update_data = technician.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_technician, field, value)
        db.commit()
        db.refresh(db_technician)
    return db_technician

def delete_existing_technician(db: Session, technician_id: int):
    db_technician = db.query(Technician).filter(Technician.id == technician_id).first()
    if db_technician:
        db.delete(db_technician)
        db.commit()
        return True
    return False

# Booking CRUD operations
def get_all_bookings(db: Session):
    return db.query(Booking).all()

def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def create_new_booking(db: Session, booking: BookingCreate):
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_existing_booking(db: Session, booking_id: int, booking: BookingUpdate):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        update_data = booking.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_booking, field, value)
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_existing_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return True
    return False

# Feedback CRUD operations
def get_all_feedback(db: Session):
    return db.query(Feedback).all()

def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

def create_new_feedback(db: Session, feedback: FeedbackCreate):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_existing_feedback(db: Session, feedback_id: int, feedback: FeedbackUpdate):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        update_data = feedback.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_feedback, field, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_existing_feedback(db: Session, feedback_id: int):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
        return True
    return False

# Admin user CRUD operations
def create_admin_user(db: Session, admin_user: AdminUserCreate):
    hashed_password = get_password_hash(admin_user.password)
    db_admin_user = AdminUser(
        email=admin_user.email,
        hashed_password=hashed_password,
        is_active=admin_user.is_active
    )
    db.add(db_admin_user)
    db.commit()
    db.refresh(db_admin_user)
    return db_admin_user

def get_admin_user_by_email(db: Session, email: str):
    return db.query(AdminUser).filter(AdminUser.email == email).first()
