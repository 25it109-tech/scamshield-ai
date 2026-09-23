import os
import base64
import time
import requests
import whois
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

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
    Combines both checks into one result.
    """
    reputation = check_url_reputation(url)
    age = check_domain_age(url)

    return {
        "url": url,
        "malicious": reputation.get("malicious", False),
        "flagged_count": reputation.get("flagged_count", 0),
        "domain_age_days": age.get("domain_age_days"),
    }


if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "https://sbi-secure-verification-login.com",
    ]
    for u in test_urls:
        print(u, "->", check_url(u))