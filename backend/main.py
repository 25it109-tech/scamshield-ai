from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if APP_ROOT not in sys.path:
    sys.path.append(APP_ROOT)

from database import save_scan_result
from security.security_check import get_risk_assessment

# ---------- App setup ----------
app = FastAPI(title="ScamShield AI API")

# ---------- CORS setup (so frontend can call this backend) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Request model ----------
class ScanRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    image_base64: Optional[str] = None


# ---------- Response model ----------
class ScanResponse(BaseModel):
    risk_level: str
    what: str
    why: List[str]
    action: List[str]


# ---------- Health check route ----------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------- Scan route ----------
@app.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    try:
        result = get_risk_assessment(
            user_input=request.text or "",
            url=request.url,
        )

        if "error" in result:
            return ScanResponse(
                risk_level="UNKNOWN",
                what="Analysis unavailable",
                why=[result.get("error", "Unknown error")],
                action=["Please try again later"],
            )

        save_scan_result(
            input_text=request.text,
            input_url=request.url,
            risk_level=result.get("risk_level", "UNKNOWN"),
            what=result.get("what", ""),
            why=", ".join(result.get("why", [])),
            action=", ".join(result.get("action", [])),
        )

        return ScanResponse(
            risk_level=result.get("risk_level", "UNKNOWN"),
            what=result.get("what", "No details available"),
            why=result.get("why", []),
            action=result.get("action", []),
        )

    except Exception as e:
        return ScanResponse(
            risk_level="UNKNOWN",
            what="Error occurred during analysis",
            why=[str(e)],
            action=["Please try again"],
        )
