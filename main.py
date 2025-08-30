from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Mahadeva Electronics API",
    description="FastAPI backend for Mahadeva Electronics website",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables when the app starts"""
    try:
        from database import engine
        from models import Base
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully on startup")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not create database tables on startup: {e}")
        print("Tables will be created when first accessed")

@app.get("/")
async def root():
    return {
        "message": "Mahadeva Electronics API",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from database import engine
        from sqlalchemy import text
        
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "message": "API is running",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": "API is running but database connection failed",
            "database": "disconnected",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }

# Import CRUD functions
from database import get_db
from models import Base
from schemas import *
from crud import *

# Product routes
@app.get("/api/products/", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    try:
        return get_all_products(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get products: {str(e)}")

@app.post("/api/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_new_product(db, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get product: {str(e)}")

@app.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        updated_product = update_existing_product(db, product_id, product)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_existing_product(db, product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")

# Image upload endpoint for products
@app.post("/api/products/{product_id}/upload_images/")
async def upload_product_images(
    product_id: int, 
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Check if product exists
        product = get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # For now, just return success (you can implement actual file storage later)
        uploaded_files = []
        for file in files:
            if file.filename:
                uploaded_files.append(file.filename)
        
        return {
            "message": "Images uploaded successfully",
            "product_id": product_id,
            "uploaded_files": uploaded_files
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload images: {str(e)}")

# Part routes
@app.get("/api/parts/", response_model=List[PartResponse])
async def get_parts(db: Session = Depends(get_db)):
    try:
        return get_all_parts(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get parts: {str(e)}")

@app.post("/api/parts/", response_model=PartResponse)
async def create_part(part: PartCreate, db: Session = Depends(get_db)):
    try:
        return create_new_part(db, part)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create part: {str(e)}")

@app.get("/api/parts/{part_id}", response_model=PartResponse)
async def get_part(part_id: int, db: Session = Depends(get_db)):
    try:
        part = get_part_by_id(db, part_id)
        if not part:
            raise HTTPException(status_code=404, detail="Part not found")
        return part
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get part: {str(e)}")

@app.put("/api/parts/{part_id}", response_model=PartResponse)
async def update_part(part_id: int, part: PartUpdate, db: Session = Depends(get_db)):
    try:
        updated_part = update_existing_part(db, part_id, part)
        if not updated_part:
            raise HTTPException(status_code=404, detail="Part not found")
        return updated_part
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update part: {str(e)}")

@app.delete("/api/parts/{part_id}")
async def delete_part(part_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_existing_part(db, part_id)
        if not success:
            raise HTTPException(status_code=500, detail="Part not found")
        return {"message": "Part deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete part: {str(e)}")

# Technician routes
@app.get("/api/technicians/", response_model=List[TechnicianResponse])
async def get_technicians(db: Session = Depends(get_db)):
    try:
        return get_all_technicians(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get technicians: {str(e)}")

@app.post("/api/technicians/", response_model=TechnicianResponse)
async def create_technician(technician: TechnicianCreate, db: Session = Depends(get_db)):
    try:
        return create_new_technician(db, technician)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create technician: {str(e)}")

@app.put("/api/technicians/{technician_id}", response_model=TechnicianResponse)
async def update_technician(technician_id: int, technician: TechnicianUpdate, db: Session = Depends(get_db)):
    try:
        updated_technician = update_existing_technician(db, technician_id, technician)
        if not updated_technician:
            raise HTTPException(status_code=404, detail="Technician not found")
        return updated_technician
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update technician: {str(e)}")

@app.delete("/api/technicians/{technician_id}")
async def delete_technician(technician_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_existing_technician(db, technician_id)
        if not success:
            raise HTTPException(status_code=404, detail="Technician not found")
        return {"message": "Technician deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete technician: {str(e)}")

# Booking routes
@app.get("/api/bookings/", response_model=List[BookingResponse])
async def get_bookings(db: Session = Depends(get_db)):
    try:
        return get_all_bookings(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get bookings: {str(e)}")

@app.post("/api/bookings/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        return create_new_booking(db, booking)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create booking: {str(e)}")

@app.put("/api/bookings/{booking_id}", response_model=BookingResponse)
async def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    try:
        updated_booking = update_existing_booking(db, booking_id, booking)
        if not updated_booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return updated_booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update booking: {str(e)}")

@app.delete("/api/bookings/{booking_id}")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_existing_booking(db, booking_id)
        if not success:
            raise HTTPException(status_code=404, detail="Booking not found")
        return {"message": "Booking deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete booking: {str(e)}")

# Technician assignment endpoint for bookings
@app.post("/api/bookings/{booking_id}/assign/")
async def assign_technician_to_booking(
    booking_id: int,
    assignment: dict,  # {"technician_id": int}
    db: Session = Depends(get_db)
):
    try:
        # Check if booking exists
        booking = get_booking_by_id(db, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Check if technician exists
        technician = get_technician_by_id(db, assignment.get("technician_id"))
        if not technician:
            raise HTTPException(status_code=404, detail="Technician not found")
        
        # Update booking with technician assignment
        # You can implement this in your CRUD functions
        return {
            "message": "Technician assigned successfully",
            "booking_id": booking_id,
            "technician_id": assignment.get("technician_id")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign technician: {str(e)}")

# Feedback routes
@app.get("/api/feedback/", response_model=List[FeedbackResponse])
async def get_feedback(db: Session = Depends(get_db)):
    try:
        return get_all_feedback(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feedback: {str(e)}")

@app.post("/api/feedback/", response_model=FeedbackResponse)
async def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        return create_new_feedback(db, feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create feedback: {str(e)}")

@app.put("/api/feedback/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(feedback_id: int, feedback: FeedbackUpdate, db: Session = Depends(get_db)):
    try:
        updated_feedback = update_existing_feedback(db, feedback_id, feedback)
        if not updated_feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return updated_feedback
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update feedback: {str(e)}")

@app.delete("/api/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_existing_feedback(db, feedback_id)
        if not success:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return {"message": "Feedback deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete feedback: {str(e)}")

# Authentication routes
@app.post("/api/auth/token/")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
