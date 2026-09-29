🚨 Incident Response Agent
An AI-powered incident management and memory system designed to help engineering teams record, investigate, resolve, and learn from production incidents.

The system maintains a memory of previous incidents, including symptoms, root causes, resolutions, and operational knowledge, so engineers can use historical incidents to respond to future problems more efficiently.

✨ Features
📝 Incident Management

Create and track production incidents
Store incident descriptions, services, severity, and status
Track open and resolved incidents
🧠 Incident Memory

Store previous incidents and their resolutions
Preserve root-cause information
Use historical incidents as operational knowledge
🤖 AI-Assisted Response

Analyze incident information using Google's Generative AI
Provide context based on previous incidents
Assist engineers during incident investigation
🗄️ PostgreSQL Database

Persistent incident storage
SQLAlchemy-based database layer
⚡ FastAPI Backend

REST API for incident operations
Automatic API documentation
Modular backend architecture
💻 React Frontend

Modern incident operations dashboard
Incident overview and status information
Recent incident memory
🏗️ Architecture
                    ┌──────────────────────┐
                    │      React UI        │
                    │      Vite            │
                    └──────────┬───────────┘
                               │
                               │ REST API
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌──────────────┐  ┌─────────────┐
       │ PostgreSQL  │  │  SQLAlchemy  │  │ Google GenAI│
       │  Database   │  │     ORM      │  │     AI      │
       └─────────────┘  └──────────────┘  └─────────────┘
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
HTML
CSS
Backend
Python
FastAPI
Uvicorn
SQLAlchemy
Pydantic
Database
PostgreSQL
Psycopg
AI
Google Generative AI / Gemini
Development
Git
GitHub
Python Virtual Environment
npm
📁 Project Structure
incident-response-agent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── incidents.py
│   │   │
│   │   ├── database/
│   │   │   └── connection.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
🚀 Getting Started
1. Clone the repository
git clone https://github.com/Charanrakesh/incident-response-agent.git
cd incident-response-agent
2. Backend Setup
Create a Python virtual environment:

Windows
python -m venv .venv
Activate it:

.\.venv\Scripts\Activate.ps1
Install the dependencies:

cd backend
python -m pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the backend directory.

Example:

DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/incident_db

GOOGLE_API_KEY=your_google_api_key
⚠️ Security
Never commit .env files, API keys, passwords, database credentials, or tokens to GitHub.

Make sure .env is included in .gitignore.

4. Start PostgreSQL
Make sure PostgreSQL is installed and running.

Create the database configured in your DATABASE_URL.

For example:

incident_db
The application uses SQLAlchemy to communicate with PostgreSQL.

5. Start the Backend
From the backend directory:

python -m uvicorn app.main:app --reload
The backend will run at:

http://127.0.0.1:8000
FastAPI documentation:

http://127.0.0.1:8000/docs
Alternative documentation:

http://127.0.0.1:8000/redoc
🎨 Frontend Setup
Open a new terminal.

Go to the frontend:

cd incident-response-agent\frontend
Install dependencies:

npm install
Start the development server:

npm run dev
The frontend will normally be available at:

http://localhost:5173
🔄 Running the Complete Application
You need two terminals.

Terminal 1 — Backend
cd incident-response-agent
.\.venv\Scripts\Activate.ps1
cd backend
python -m uvicorn app.main:app --reload
Terminal 2 — Frontend
cd incident-response-agent\frontend
npm run dev
Then open the frontend URL shown by Vite.

📡 API
The backend exposes REST endpoints for incident management.

The complete API can be explored through FastAPI Swagger:

http://127.0.0.1:8000/docs
Typical operations include:

POST    /incidents
GET     /incidents
GET     /incidents/{id}
PUT     /incidents/{id}
DELETE  /incidents/{id}
The exact available endpoints depend on the current implementation in the backend.

🧠 How the Incident Memory Works
The system is designed around the idea that previous incidents contain valuable operational knowledge.

A typical workflow is:

New Incident
     │
     ▼
Incident Details
     │
     ▼
Search Historical Incidents
     │
     ▼
Identify Similar Problems
     │
     ▼
AI-Assisted Analysis
     │
     ▼
Root Cause
     │
     ▼
Resolution
     │
     ▼
Store Incident Memory
Over time, the incident database becomes a knowledge base containing information about previous production problems.

📊 Incident Lifecycle
An incident can move through states such as:

OPEN
  │
  ▼
INVESTIGATING
  │
  ▼
RESOLVED
The system can use information from resolved incidents to assist with future incidents.

🔐 Environment & Security
Sensitive information should be stored using environment variables.

Never commit:

.env
*.env
API keys
database passwords
GitHub tokens
credentials
The repository's .gitignore should exclude these files.

🧪 Development
Backend:

cd backend
python -m uvicorn app.main:app --reload
Frontend:

cd frontend
npm run dev
📌 Current Status
The project is currently under active development.

Implemented
 FastAPI backend
 PostgreSQL database integration
 SQLAlchemy database layer
 Incident API
 React/Vite frontend
 Incident dashboard
 Google Generative AI integration
 Basic incident memory functionality
Planned Improvements
 Advanced incident similarity search
 Better AI-generated root-cause analysis
 Automated runbook recommendations
 Authentication and authorization
 Incident timeline
 Advanced analytics
 Production deployment
 Automated testing
 CI/CD pipeline
 Observability and monitoring
🎯 Project Goal
The goal of the Incident Response Agent is to transform incident handling from a purely reactive process into a memory-driven engineering workflow.

Instead of engineers repeatedly solving the same classes of problems from scratch, the system aims to preserve organizational knowledge and make previous incident experience available when it matters.

👨‍💻 Author
Charanrakesh

GitHub:

https://github.com/Charanrakesh

📄 License
This project is currently intended as a development and learning project.

A formal open-source license can be added when the project is ready for public distribution. Screenshot (64)
