from database import SessionLocal
from models import User, Resume, Job
from sqlalchemy.sql import func

def seed_data():
    db = SessionLocal()
    
    try:
        # Create a test user
        user = User(name="Test User", email="test@example.com", password_hash="hashed_password")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create a test resume
        resume = Resume(
            user_id=user.user_id,
            resume_text="Experienced Python developer with 5 years of experience in web development using Django and Flask. Proficient in SQL, JavaScript, and React. Experience with Docker and AWS. Strong background in machine learning with scikit-learn and pandas. Familiar with Git, Linux, and REST API development.",
            uploaded_at=func.now()
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        # Create test jobs
        jobs = [
            Job(
                title="Senior Python Developer",
                description="Looking for a senior Python developer with experience in Django, Flask, SQL, and cloud technologies like AWS. Knowledge of Docker and CI/CD is a plus. Must have experience with Git and Linux environments.",
                posted_at=func.now()
            ),
            Job(
                title="Full Stack Developer",
                description="Seeking a full-stack developer proficient in React, Node.js, Python, and PostgreSQL. Experience with REST APIs and microservices architecture preferred. Knowledge of JavaScript, HTML, CSS, and modern web frameworks required.",
                posted_at=func.now()
            ),
            Job(
                title="Data Scientist",
                description="Looking for a data scientist with expertise in Python, machine learning, pandas, numpy, and scikit-learn. Experience with TensorFlow or PyTorch is required. Knowledge of SQL and data visualization tools preferred.",
                posted_at=func.now()
            ),
            Job(
                title="DevOps Engineer",
                description="Seeking a DevOps engineer with experience in AWS, Docker, Kubernetes, and CI/CD pipelines. Knowledge of Terraform, Ansible, and monitoring tools. Linux administration skills required.",
                posted_at=func.now()
            ),
            Job(
                title="Frontend Developer",
                description="Looking for a frontend developer skilled in React, JavaScript, TypeScript, HTML, CSS, and modern build tools like Webpack. Experience with testing frameworks like Jest preferred.",
                posted_at=func.now()
            )
        ]
        
        for job in jobs:
            db.add(job)
        
        db.commit()
        print("✅ Seed data created successfully!")
        print(f"Created user: {user.name} (ID: {user.user_id})")
        print(f"Created resume: ID {resume.resume_id}")
        print(f"Created {len(jobs)} jobs")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

