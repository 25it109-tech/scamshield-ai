from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Make the backend package directory available when running from the venv folder.
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from database import save_scan_result

# ---------- App setup ----------
app = FastAPI(title="ScamShield AI API")

# ---------- CORS setup (so frontend can call this backend) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # for hackathon speed; restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request model ----------
class ScanRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    image_base64: Optional[str] = None  # base64-encoded image, if uploaded

# ---------- Response model ----------
from typing import List

class ScanResponse(BaseModel):
    risk_level: str
    what: str
    why: List[str]
    action: List[str]
# ---------- Health check route ----------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ---------- Scan route (hardcoded fake response for now) ----------
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from security.security_check import get_risk_assessment
from database import save_scan_result

@app.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    try:
        result = get_risk_assessment(
            user_input=request.text or "",
            url=request.url
        )

        if "error" in result:
            return ScanResponse(
                risk_level="UNKNOWN",
                what="Analysis unavailable",
                why=[result.get("error", "Unknown error")],
                action=["Please try again later"]
            )
        save_scan_result(
            input_text=request.text,
            input_url=request.url,
            risk_level=result.get("risk_level", "UNKNOWN"),
            what=result.get("what", ""),
            why=", ".join(result.get("why", [])),
            action=", ".join(result.get("action", []))
        )

        return ScanResponse(
            risk_level=result.get("risk_level", "UNKNOWN"),
            what=result.get("what", "No details available"),
            why=result.get("why", []),
            action=result.get("action", [])
        )
        

    except Exception as e:
        return ScanResponse(
            risk_level="UNKNOWN",
            what="Error occurred during analysis",
            why=[str(e)],
            action=["Please try again"]
        )