# Resume-Job Compatibility Matcher

A full-stack application that analyzes resume compatibility with job postings using skill matching algorithms.

## Features

- **Resume Upload**: Upload PDF/DOC files with automatic text extraction
- **Job Browsing**: View available job postings
- **Compatibility Analysis**: Get detailed match scores and skill analysis
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Comprehensive Skill Detection**: Advanced skill matching with 50+ technology categories

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database for storing resumes, jobs, and matches
- **SQLAlchemy**: ORM for database operations
- **PyPDF2 & python-docx**: Text extraction from resume files

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL database**:
   - Create a database named `resume_match`
   - Update the connection string in `main.py` if needed:
     ```python
     DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost/resume_match"
     ```

5. **Run database migrations and seed data**:
   ```bash
   python seed.py
   ```

6. **Start the backend server**:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

## Usage

1. **Upload Resume**: Go to `/upload_resume` and upload a PDF or DOC file
2. **Browse Jobs**: Visit `/jobs` to see available job postings
3. **Check Compatibility**: Click "Check Compatibility" on any job to see detailed analysis
4. **View Results**: Get comprehensive match scores, matched skills, and missing skills

## API Endpoints

### Backend API (http://127.0.0.1:8000)

- `GET /` - Health check
- `POST /upload_resume` - Upload resume file
- `GET /jobs` - List all jobs
- `POST /jobs` - Create new job
- `POST /match` - Calculate compatibility score
- `GET /match/{resume_id}/{job_id}` - Get match result

## Project Structure

```
resume-job-compatibility/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── matcher.py           # Skill matching algorithm
│   ├── text_extractor.py    # PDF/DOC text extraction
│   ├── seed.py              # Database seeding
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js app router pages
│   │   └── components/      # React components
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## Skill Categories

The application recognizes skills across multiple categories:

- **Programming Languages**: Python, Java, JavaScript, TypeScript, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, R, Scala, Perl, Bash, PowerShell
- **Web Technologies**: HTML, CSS, React, Angular, Vue, Node.js, Express, Django, Flask, Spring, Laravel, jQuery, Bootstrap, Sass, Less, Webpack, Babel
- **Databases**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, Oracle, SQLite, Cassandra, DynamoDB, Neo4j, Firebase
- **Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, Git, GitHub, GitLab, CI/CD, Terraform, Ansible, Chef, Puppet, Vagrant
- **Data Science & ML**: Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Jupyter, Spark, Hadoop, Kafka
- **Mobile Development**: Android, iOS, React Native, Flutter, Xamarin, Ionic
- **Testing**: Unit Testing, Integration Testing, Selenium, Cypress, Jest, Pytest, JUnit
- **Other**: Linux, Windows, macOS, REST API, GraphQL, Microservices, Agile, Scrum, Project Management, Leadership, Communication, Problem Solving

## Development

### Adding New Skills
Edit `backend/matcher.py` to add new skills to the `SKILLS` list.

### Customizing Matching Algorithm
Modify the `calculate_match` function in `backend/matcher.py` to adjust scoring logic.

### Styling
The frontend uses Tailwind CSS. Modify component classes or add custom styles in `globals.css`.

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Ensure PostgreSQL is running and the connection string is correct
2. **File Upload Fails**: Check that the uploads directory exists and has proper permissions
3. **Text Extraction Issues**: Ensure PyPDF2 and python-docx are installed correctly
4. **CORS Errors**: The backend is configured to allow all origins in development

### Logs
- Backend logs: Check terminal where uvicorn is running
- Frontend logs: Check browser console and terminal where npm run dev is running

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
