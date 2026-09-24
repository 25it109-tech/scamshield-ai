# ScamShield AI

ScamShield AI is a tool that helps detect and flag potential online scams — analyzing [messages/URLs/emails — specify what it checks] using AI and threat-intelligence APIs to warn users before they fall victim to fraud.

## Features

- [e.g., Scan URLs for malicious/phishing content using VirusTotal]
- [e.g., Analyze suspicious messages using AI (OpenRouter/LLM) to detect scam patterns]
- [e.g., Real-time risk scoring and explanation]
- [Add/remove based on what your app actually does]

## Tech Stack

**Frontend:** React (Vite)
**Backend:** FastAPI (Python)
**Database:** SQLite
**APIs used:** OpenRouter API, VirusTotal API

## Project Structure
scamshield-ai/
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ ├── scamshield.db
│ └── .env.example
├── src/
│ ├── App.jsx
│ └── components/
├── package.json
├── vite.config.js
└── README.md


## Prerequisites

- Python 3.10 or higher
- Node.js (v18 or higher) and npm

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/scamshield-ai.git
cd scamshield-ai
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder with the following:

OPENROUTER_API_KEY=your_openrouter_api_key
VT_API_KEY=your_virustotal_api_key
DATABASE_URL=sqlite:///./scamshield.db


Start the backend server:

```bash
uvicorn main:app --reload
```

The backend will run at `http://localhost:8000`.

### 3. Frontend Setup

Open a new terminal window, then from the project root:

```bash
npm install
npm run dev
```

The frontend will run at `http://localhost:5173`.

## Usage

1. Open the app in your browser at `http://localhost:5173`.
2. Paste a suspicious message, link, or text into the input field.
3. Click **Analyze** to run the scan.
4. Review the risk score and explanation provided to determine if the content is likely a scam.

## API Keys

This project requires free API keys from:

- [OpenRouter](https://openrouter.ai/keys) — for AI-based message analysis
- [VirusTotal](https://www.virustotal.com/gui/join-us) — for URL and threat scanning

Sign up on both platforms to generate your own keys and add them to your `.env` file as shown above.

## Team

**Team NEXORA**
