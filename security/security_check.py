
import os
import sys
import base64
import time
import requests
import whois
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

# Allow importing Yuvanesh's file from the sibling "ai" folder
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ai.llm_analyzer import analyze_with_llm

load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")
VT_BASE_URL = "https://www.virustotal.com/api/v3"


def check_domain_age(url: str) -> dict:
    try:
        domain = urlparse(url if "://" in url else f"http://{url}").netloc
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if not creation_date:
            return {"domain_age_days": None}
        if creation_date.tzinfo is not None:
            creation_date = creation_date.replace(tzinfo=None)
        age_days = (datetime.now() - creation_date).days
        return {"domain_age_days": age_days}
    except Exception as e:
        return {"domain_age_days": None, "note": str(e)}


def check_url_reputation(url: str) -> dict:
    """
    Checks a URL against VirusTotal.
    Returns whether it's malicious and how many vendors flagged it.
    Handles missing URL, bad URL, and API errors safely.
    """
    if not url or not isinstance(url, str) or url.strip() == "":
        return {"error": "no URL provided", "malicious": False, "flagged_count": 0}

    if not VT_API_KEY:
        return {"error": "VT_API_KEY not set", "malicious": False, "flagged_count": 0}

    try:
        headers = {"x-apikey": VT_API_KEY}
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        resp = requests.get(f"{VT_BASE_URL}/urls/{url_id}", headers=headers, timeout=10)

        if resp.status_code == 404:
            submit = requests.post(f"{VT_BASE_URL}/urls", headers=headers, data={"url": url}, timeout=10)
            submit.raise_for_status()
            analysis_id = submit.json()["data"]["id"]

            for _ in range(5):
                time.sleep(2)
                analysis = requests.get(f"{VT_BASE_URL}/analyses/{analysis_id}", headers=headers, timeout=10)
                if analysis.json()["data"]["attributes"]["status"] == "completed":
                    stats = analysis.json()["data"]["attributes"]["stats"]
                    break
            else:
                return {"error": "scan timed out", "malicious": False, "flagged_count": 0}
        else:
            resp.raise_for_status()
            stats = resp.json()["data"]["attributes"]["last_analysis_stats"]

        flagged_count = stats.get("malicious", 0) + stats.get("suspicious", 0)

        return {
            "malicious": flagged_count > 0,
            "flagged_count": flagged_count,
            "harmless_count": stats.get("harmless", 0),
        }

    except Exception as e:
        return {"error": str(e), "malicious": False, "flagged_count": 0}


def check_url(url: str) -> dict:
    """
    Combines VirusTotal + domain age into one result.
    """
    reputation = check_url_reputation(url)
    age = check_domain_age(url)

    return {
        "url": url,
        "malicious": reputation.get("malicious", False),
        "flagged_count": reputation.get("flagged_count", 0),
        "domain_age_days": age.get("domain_age_days"),
    }


def get_risk_assessment(user_input, url=None):
    """
    Combines Subasri's URL check with Yuvanesh's AI text analysis
    into one final risk verdict.
    """
    ai_result = analyze_with_llm(user_input)

    url_result = None
    if url:
        url_result = check_url(url)

    # If AI call failed, fall back to just the URL check
    if "error" in ai_result:
        if url_result and url_result["malicious"]:
            final_risk = "HIGH"
        else:
            final_risk = "UNKNOWN"
        return {
            "risk_level": final_risk,
            "why": ["AI analysis unavailable"],
            "action": ["Proceed with caution"],
            "url_check": url_result,
        }

    final_risk = ai_result.get("risk_level", "LOW")

    # Bump risk up if the URL is known malicious or the domain is very new
    if url_result:
        if url_result.get("malicious"):
            final_risk = "HIGH"
        elif url_result.get("domain_age_days") is not None and url_result["domain_age_days"] < 30:
            if final_risk == "LOW":
                final_risk = "MEDIUM"

    return {
        "risk_level": final_risk,
        "confidence": ai_result.get("confidence"),
        "what": ai_result.get("what"),
        "why": ai_result.get("why", []),
        "action": ai_result.get("action", []),
        "url_check": url_result,
    }


if __name__ == "__main__":
    test_message = "Your SBI account will be blocked in 24 hours. Verify now to avoid suspension."
    test_url = "https://sbi-secure-verification-login.com"

    result = get_risk_assessment(test_message, test_url)
    print(result)