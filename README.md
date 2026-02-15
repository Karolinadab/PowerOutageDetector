# PowerOutageDetector

Small console app that runs in the background and polls the power-outage API on scheduled hours.

## Requirements
- Python 3.11+

## Local setup
1. Create and activate a virtual environment. Example:
	- `py -m venv .venv`
	- `.venv\Scripts\activate`
2. Install dependencies:
	- `pip install -r requirements.txt`
3. Create a `.env` file based on `.env.example`.

## Run
From the repo root:
- `python -m power_outage_detector`

## Docker
Build the image from the repo root:
- `docker build -t power-outage-detector .`

Run with your `.env` file:
- `docker run --rm --env-file .env power-outage-detector`
