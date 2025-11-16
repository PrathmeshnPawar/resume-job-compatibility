from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Resume, Job, Match
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
import os

# ------------------------
# Database setup
# ------------------------
DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost/resume_match"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if not already created
Base.metadata.create_all(bind=engine)

# ------------------------
# FastAPI app setup
# ------------------------
app = FastAPI()

# CORS (frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# Routes
# ------------------------
@app.get("/")
def root():
    return {"message": "Resume Matcher Backend is running 🚀"}


# Create user
@app.post("/users")
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password_hash: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        new_user = User(name=name, email=email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Upload resume
@app.post("/upload_resume")
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    os.makedirs("uploads", exist_ok=True)

    # Save file locally
    file_path = f"uploads/{resume.filename}"
    contents = await resume.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Extract text from the uploaded file
    from text_extractor import extract_text_from_file, clean_extracted_text
    
    extracted_text = extract_text_from_file(file_path)
    if extracted_text:
        resume_text = clean_extracted_text(extracted_text)
    else:
        resume_text = f"Resume content from {resume.filename}. Text extraction failed, using filename as placeholder."

    # Store in DB (using user_id=1 as default for demo)
    new_resume = Resume(
        user_id=1,  # Default user for demo
        resume_text=resume_text,
        uploaded_at=func.now(),
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "filename": resume.filename,
        "resume_id": new_resume.resume_id,
        "status": "uploaded",
    }


# Add job
@app.post("/jobs")
def create_job(
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):
    new_job = Job(title=title, description=description)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


# List jobs
@app.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


# List resumes
@app.get("/resumes")
def list_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).all()


# Match resume with job
@app.post("/match")
def match_resume_job(
    resume_id: int = Form(...),
    job_id: int = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # Get resume and job
        resume = db.query(Resume).filter(Resume.resume_id == resume_id).first()
        job = db.query(Job).filter(Job.job_id == job_id).first()
        
        if not resume or not job:
            raise HTTPException(status_code=404, detail="Resume or job not found")
        
        # Import matcher functions
        from matcher import calculate_match
        
        # Calculate match
        score, matched_skills, missing_skills = calculate_match(resume.resume_text, job.description)
        
        # Create match record
        match = Match(
            resume_id=resume_id,
            job_id=job_id,
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )
        db.add(match)
        db.commit()
        db.refresh(match)
        
        return {
            "match_id": match.match_id,
            "score": float(score),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "resume_title": f"Resume {resume_id}",
            "job_title": job.title
        }
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Get match result
@app.get("/match/{resume_id}/{job_id}")
def get_match_result(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(
        Match.resume_id == resume_id,
        Match.job_id == job_id
    ).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return {
        "score": float(match.score),
        "matched_skills": match.matched_skills,
        "missing_skills": match.missing_skills,
        "analyzed_at": match.analyzed_at
    }
