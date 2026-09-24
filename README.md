# ScamShield AI

ScamShield AI is a web application that helps users identify potentially fraudulent or malicious content. It analyzes suspicious messages and URLs using AI-based scam detection and threat-intelligence services, then provides a risk assessment and explanation.

> **Note:** Do not commit real API keys. Store them only in a local `.env` file.

## Features

- Analyze suspicious messages and text for common scam patterns.
- Scan URLs for potential malicious or phishing activity using VirusTotal.
- Use an LLM through OpenRouter for AI-assisted analysis.
- Provide a risk score and an explanation of the result.
- Store application data in a local SQLite database.

## Tech Stack

- **Frontend:** React with Vite
- **Backend:** FastAPI with Python
- **Database:** SQLite
- **APIs:** OpenRouter and VirusTotal

## Project Structure

```text
scamshield-ai/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── scamshield.db
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm
- An OpenRouter API key
- A VirusTotal API key

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/25it109-tech/scamshield-ai.git
cd scamshield-ai
```

### 2. Configure the backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Linux/macOS
source venv/bin/activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Create a file named `.env` inside the `backend/` directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
VT_API_KEY=your_virustotal_api_key
DATABASE_URL=sqlite:///./scamshield.db
```

Start the backend server from the `backend/` directory:

```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`.

### 3. Configure the frontend

Open a new terminal and run:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Usage

1. Open `http://localhost:5173` in your browser.
2. Enter a suspicious message, URL, or other supported text.
3. Click **Analyze**.
4. Review the risk score and explanation.

## API Keys

Create API keys from the following services:

- [OpenRouter](https://openrouter.ai/keys) — AI-based message analysis
- [VirusTotal](https://www.virustotal.com/gui/join-us) — URL and threat scanning

Add the keys to `backend/.env`. The `.env` file should not be committed to Git.

## Team

**Team NEXORA**
