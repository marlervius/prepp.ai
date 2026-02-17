"""
Simplified Prepp.ai FastAPI Backend for initial testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import time
import uuid

app = FastAPI(
    title="Prepp.ai API (Simple)",
    description="Simplified version for initial testing",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BriefRequest(BaseModel):
    """Request model for generating a brief"""
    subject: str
    grade: str
    topic: str

class BriefResponse(BaseModel):
    """Response model for generated brief"""
    id: str
    subject: str
    grade: str
    topic: str
    content: Dict[str, Any]
    sources: List[Dict[str, str]]
    processing_time_ms: int
    created_at: str

# Mock data for testing
MOCK_BRIEF_CONTENT = {
    "lk20_kobling": "Dette emnet er knyttet til LK20 kompetansemål i naturfag for trinnet du underviser. Eleven skal kunne utforske, forklare og forutsi bevegelser og krefter ved hjelp av Newtons lover og energibegreper.",
    "faglig_dybde": "Fotosyntese er den prosessen hvor grønne planter, alger og noen bakterier lager organisk materiale fra uorganiske stoffer ved hjelp av lysenergi. Karbondioksid og vann omdannes til glukose og oksygen i kloroplastene i plantecellene.",
    "pedagogiske_tips": "Bruk analogien med et kjøkken hvor planter er kokker som lager mat. Diskuter hvorfor planter er grønne og hvorfor vi trenger planter for å overleve. La elevene plante frø og observere vekstprosessen.",
    "elev_sporsmal_feller": "Vanlige spørsmål: 'Kan planter lage mat uten lys?' Svar: Nei, fotosyntese krever lysenergi. Felles misforståelse: 'Planter spiser gjennom røttene' - forklar at de absorberer vann og mineraler, men lager maten selv.",
    "kilder": "Basert på Store norske leksikon, NDLA og Utdanningsdirektoratets læreplaner. Se snl.no/fotosyntese og ndla.no for mer informasjon."
}

@app.post("/api/v1/briefs", response_model=BriefResponse)
async def generate_brief(request: BriefRequest) -> BriefResponse:
    """
    Generate a mock teaching brief for testing
    """
    start_time = time.time()

    # Simulate processing time
    import asyncio
    await asyncio.sleep(2)

    processing_time = int((time.time() - start_time) * 1000)

    # Create mock response
    brief_data = {
        "id": str(uuid.uuid4()),
        "subject": request.subject,
        "grade": request.grade,
        "topic": request.topic,
        "content": MOCK_BRIEF_CONTENT,
        "sources": [
            {
                "title": f"{request.topic} - {request.subject}",
                "url": f"https://ndla.no/emne/{request.subject.lower()}",
                "source": "ndla"
            }
        ],
        "processing_time_ms": processing_time,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    return BriefResponse(**brief_data)

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "prepp-ai-backend-simple"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Prepp.ai Simple API",
        "version": "0.1.0",
        "status": "running",
        "note": "This is a simplified version for testing. Full AI functionality requires API keys."
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Prepp.ai Simple Backend...")
    print("API will be available at: http://localhost:8000")
    print("Frontend should be running at: http://localhost:3000")
    uvicorn.run(
        "app.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )