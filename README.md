# E-REDES Storm Kristin Chatbot

Portuguese-language customer support chatbot for E-REDES power outage information during Storm Kristin (January 28, 2026).

Uses **Groq** (Llama 3.3 70B) with function calling to query the real E-REDES scheduled interruptions API and mock storm outage data for 7 affected districts.

## Architecture

```
Browser (HTML/CSS/JS)  <-->  FastAPI Backend  <-->  Groq (Llama 3.3 70B)
                                   |                       |
                             Mock Outage DB          E-REDES Open Data API
```

## Features

- Real-time query of E-REDES Open Data API for scheduled interruptions
- Mock storm outage data for 7 affected districts (Leiria, Coimbra, Castelo Branco, Portalegre, Santarém, Viseu, Guarda)
- Location lookup by postal code, district, or municipality name
- National impact summary (175,000 customers affected)
- Safety advice (downed lines, generators, food safety, heating)
- Compensation rights information (ERSE regulations)
- E-REDES branded responsive frontend

## Setup

```bash
pip install -r requirements.txt
export GROQ_API_KEY='your-key-here'
uvicorn app:app --host 0.0.0.0 --port 8000
```

Get a free Groq API key at https://console.groq.com/keys

Then open http://localhost:8000

## Project Structure

```
app.py              # FastAPI app, /api/chat endpoint with tool-call loop
config.py           # Config constants (API URLs, model, contacts)
eredes_api.py       # Real E-REDES Open Data API client (scheduled interruptions)
outage_data.py      # Mock Storm Kristin outage database by district
openai_tools.py     # Tool definitions + handler (3 tools)
system_prompt.py    # Portuguese system prompt with storm context & safety advice
requirements.txt    # Python dependencies
static/
  index.html        # Chat widget page with E-REDES branding
  style.css         # E-REDES green (#00A651) themed responsive styles
  script.js         # Frontend chat logic
```

## Tools

The chatbot has access to 3 function-calling tools:

| Tool | Description | Data Source |
|------|-------------|-------------|
| `consultar_interrupcoes_programadas` | Scheduled maintenance interruptions | Real E-REDES API |
| `consultar_estado_tempestade_kristin` | Storm outage status by location | Mock data |
| `resumo_nacional_tempestade` | National impact summary | Mock data |
