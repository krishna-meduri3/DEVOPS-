from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

from app.database.connection import SessionLocal
from app.models.incident import Incident
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse
)


load_dotenv()


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# --------------------------------------------------
# INCIDENT ID GENERATOR
# --------------------------------------------------

def generate_incident_id(db: Session):

    last_incident = (
        db.query(Incident)
        .order_by(Incident.id.desc())
        .first()
    )

    number = (
        1
        if last_incident is None
        else last_incident.id + 1
    )

    return f"INC-{number:04d}"


# --------------------------------------------------
# CREATE INCIDENT
# --------------------------------------------------

@router.post(
    "/",
    response_model=IncidentResponse
)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):

    new_incident = Incident(
        incident_id=generate_incident_id(db),
        title=incident.title,
        description=incident.description,
        service=incident.service,
        severity=incident.severity,
        status="OPEN"
    )

    db.add(new_incident)

    db.commit()

    db.refresh(new_incident)

    return new_incident


# --------------------------------------------------
# GET ALL INCIDENTS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[IncidentResponse]
)
def get_incidents(
    db: Session = Depends(get_db)
):

    return (
        db.query(Incident)
        .order_by(Incident.id.desc())
        .all()
    )


# --------------------------------------------------
# GET SINGLE INCIDENT
# --------------------------------------------------

@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(Incident)
        .filter(
            Incident.incident_id == incident_id
        )
        .first()
    )

    if incident is None:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


# --------------------------------------------------
# UPDATE INCIDENT
# --------------------------------------------------

@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse
)
def update_incident(
    incident_id: str,
    update: IncidentUpdate,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(Incident)
        .filter(
            Incident.incident_id == incident_id
        )
        .first()
    )

    if incident is None:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    fields = [
        "title",
        "description",
        "service",
        "severity",
        "status",
        "root_cause",
        "resolution"
    ]

    for field in fields:

        value = getattr(
            update,
            field
        )

        if value is not None:

            setattr(
                incident,
                field,
                value
            )

    db.commit()

    db.refresh(incident)

    return incident


# --------------------------------------------------
# MEMORY SEARCH
# --------------------------------------------------

class MemorySearchRequest(BaseModel):

    query: str


@router.post(
    "/memory/search"
)
def search_memory(
    request: MemorySearchRequest,
    db: Session = Depends(get_db)
):

    query = request.query.lower().strip()

    if not query:

        return {
            "matches": [],
            "message":
                "Enter an incident description."
        }

    incidents = db.query(Incident).all()

    results = []

    query_words = set(query.split())

    for incident in incidents:

        searchable = " ".join([
            incident.title or "",
            incident.description or "",
            incident.service or "",
            incident.root_cause or "",
            incident.resolution or ""
        ]).lower()

        matched_words = [
            word
            for word in query_words
            if len(word) > 2
            and word in searchable
        ]

        if matched_words:

            score = round(
                (
                    len(matched_words)
                    /
                    max(len(query_words), 1)
                )
                * 100
            )

            results.append({

                "incident_id":
                    incident.incident_id,

                "title":
                    incident.title,

                "service":
                    incident.service,

                "severity":
                    incident.severity,

                "status":
                    incident.status,

                "root_cause":
                    incident.root_cause,

                "resolution":
                    incident.resolution,

                "similarity":
                    score

            })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return {

        "query":
            request.query,

        "matches":
            results[:5]

    }


# --------------------------------------------------
# AI INCIDENT ANALYSIS
# --------------------------------------------------

class AIAnalysisRequest(BaseModel):

    query: str


@router.post(
    "/ai/analyze"
)
def analyze_incident(
    request: AIAnalysisRequest,
    db: Session = Depends(get_db)
):

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Incident description is required."
        )

    # ----------------------------------------------
    # FIND SIMILAR INCIDENTS
    # ----------------------------------------------

    incidents = db.query(Incident).all()

    query_words = set(
        query.lower().split()
    )

    matches = []

    for incident in incidents:

        searchable = " ".join([
            incident.title or "",
            incident.description or "",
            incident.service or "",
            incident.root_cause or "",
            incident.resolution or ""
        ]).lower()

        matched_words = [
            word
            for word in query_words
            if len(word) > 2
            and word in searchable
        ]

        if matched_words:

            similarity = round(
                (
                    len(matched_words)
                    /
                    max(len(query_words), 1)
                )
                * 100
            )

            matches.append({

                "incident_id":
                    incident.incident_id,

                "title":
                    incident.title,

                "service":
                    incident.service,

                "severity":
                    incident.severity,

                "status":
                    incident.status,

                "root_cause":
                    incident.root_cause,

                "resolution":
                    incident.resolution,

                "similarity":
                    similarity

            })

    matches.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    matches = matches[:5]

    # ----------------------------------------------
    # GEMINI CLIENT
    # ----------------------------------------------

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured."
        )

    try:

        client = genai.Client(
            api_key=api_key
        )

        # ------------------------------------------
        # BUILD INCIDENT MEMORY
        # ------------------------------------------

        if matches:

            memory_text = ""

            for match in matches:

                memory_text += f"""
Incident ID:
{match["incident_id"]}

Title:
{match["title"]}

Service:
{match["service"]}

Severity:
{match["severity"]}

Status:
{match["status"]}

Similarity:
{match["similarity"]}%

Root Cause:
{match["root_cause"] or "Not documented"}

Previous Resolution:
{match["resolution"] or "Not documented"}

----------------------------------------
"""

        else:

            memory_text = (
                "No matching historical incidents "
                "were found."
            )

        # ------------------------------------------
        # AI PROMPT
        # ------------------------------------------

        prompt = f"""
You are an expert Site Reliability Engineer
and Incident Response Agent.

Analyze the following new production incident.

NEW INCIDENT:
{query}

HISTORICAL INCIDENT MEMORY:
{memory_text}

Your job is to help an engineer respond safely
and efficiently.

Return a concise incident analysis using exactly
these sections:

LIKELY ROOT CAUSE

Explain the most likely cause based ONLY on the
available incident information.

EVIDENCE

Explain which historical incidents or symptoms
support the conclusion.

RECOMMENDED ACTIONS

Give practical numbered troubleshooting and
recovery steps.

PREVIOUS SUCCESSFUL RESOLUTION

If a historical resolution exists, explain it.
If none exists, say "No previous resolution found."

CAUTION

Mention anything the engineer should verify
before performing a potentially risky action.

Do not invent infrastructure details that are not
present in the incident memory.

Clearly distinguish evidence from inference.
"""

        # ------------------------------------------
        # GEMINI
        # ------------------------------------------

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {

            "query":
                query,

            "matches":
                matches,

            "analysis":
                response.text

        }

    except Exception as error:

        print(
            "Gemini error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=
                "AI analysis failed. "
                "Check Gemini API configuration."
        )