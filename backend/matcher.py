from database import SessionLocal
from models import Resume, Job, Match
import re

# Comprehensive skill extraction
SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby", "go", "rust", "swift", "kotlin",
    "r", "scala", "perl", "bash", "powershell",
    
    # Web Technologies
    "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask", "spring", "laravel",
    "jquery", "bootstrap", "sass", "less", "webpack", "babel",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracle", "sqlite", "cassandra",
    "dynamodb", "neo4j", "firebase",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "ci/cd",
    "terraform", "ansible", "chef", "puppet", "vagrant",
    
    # Data Science & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "jupyter", "spark", "hadoop", "kafka",
    
    # Mobile Development
    "android", "ios", "react native", "flutter", "xamarin", "ionic",
    
    # Testing
    "unit testing", "integration testing", "selenium", "cypress", "jest", "pytest", "junit",
    
    # Other Technologies
    "linux", "windows", "macos", "rest api", "graphql", "microservices", "agile", "scrum",
    "project management", "leadership", "communication", "problem solving"
]

def extract_skills(text: str):
    text = text.lower()
    found_skills = []
    
    # Handle special cases and variations
    skill_variations = {
        "node.js": ["nodejs", "node js", "node"],
        "c++": ["cpp", "c plus plus"],
        "c#": ["csharp", "c sharp"],
        "machine learning": ["ml", "machinelearning"],
        "deep learning": ["dl", "deeplearning"],
        "rest api": ["rest", "api", "restful"],
        "ci/cd": ["cicd", "continuous integration", "continuous deployment"],
        "unit testing": ["unit test", "unit tests"],
        "integration testing": ["integration test", "integration tests"],
        "project management": ["pm", "project manager"],
    }
    
    # Check for exact matches and variations
    for skill in SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found_skills.append(skill)
        elif skill in skill_variations:
            for variation in skill_variations[skill]:
                if re.search(rf"\b{re.escape(variation)}\b", text):
                    found_skills.append(skill)
                    break
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(found_skills))

def calculate_match(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0
    return score, list(matched), list(missing)

def run_match():
    db = SessionLocal()

    # Get latest resume and job
    resume = db.query(Resume).first()
    job = db.query(Job).first()

    score, matched, missing = calculate_match(resume.resume_text, job.description)

    match = Match(
        resume_id=resume.resume_id,
        job_id=job.job_id,
        score=score,
        matched_skills=matched,
        missing_skills=missing,
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    print(f"✅ Match created with score {score:.2f}%")
    print(f"Matched: {matched}")
    print(f"Missing: {missing}")

if __name__ == "__main__":
    run_match()

