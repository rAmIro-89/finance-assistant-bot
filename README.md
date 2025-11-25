# 💰 Financial Assistant Chatbot

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Integration-25D366.svg)](https://www.twilio.com/whatsapp)

AI-powered conversational financial education assistant with budget simulators, interactive dashboard, and persistent user memory. Deployable on NAS with Docker, accessible via web and WhatsApp.

## Business Problem

**Objective:** Democratize financial literacy through an accessible, personalized AI assistant that helps users understand budgeting, savings, investments, and debt management.

**Real-World Applications:**
- **Financial Education:** Interactive chatbot teaches concepts like 50/30/20 rule, compound interest, investment vehicles (ETFs, mutual funds), and debt consolidation strategies
- **Budget Planning:** Personalized budget simulators that adapt to user income, expenses, and financial goals
- **Investment Guidance:** Compare investment scenarios (conservative vs aggressive portfolios) with visualizations showing long-term growth
- **Debt Management:** Calculate payoff strategies, analyze refinancing options, and provide actionable debt reduction plans
- **Multi-Channel Accessibility:** Available 24/7 via web dashboard and WhatsApp integration for on-the-go financial advice

**Target Audience:** 
- Young professionals seeking financial literacy
- Individuals wanting to improve budgeting habits
- Users exploring investment options without financial advisor costs
- Spanish-speaking (Argentina) and English-speaking markets

**Technical Challenge:** Build an NLP system that understands financial intents, maintains conversation context across sessions, persists user data securely, and delivers accurate financial calculations with interactive visualizations.

## Key Features

### Conversational AI
- **Intent Recognition:** Budget planning, savings goals, investments, debt management, financial calculators, and educational content
- **NLP Processing:** Context-aware conversation memory that spans multiple sessions
- **Multi-Language:** Supports Spanish (primary) and English
- **Slang Understanding:** Recognizes financial slang (e.g., "lucas" = thousands in Argentina)

### Interactive Dashboard
- **50/30/20 Budget Rule:** Visual breakdown of needs, wants, and savings
- **Compound Interest Calculator:** Project investment growth over time
- **Investment Comparison:** Compare conservative vs aggressive portfolio scenarios
- **Debt Analyzer:** Calculate payoff timelines and interest savings
- **Built with Plotly:** Interactive, responsive charts

### Data Persistence
- **SQLite + SQLAlchemy:** Store user income, debts, risk profile, and savings goals
- **User Identity:** Web cookie (`uid`), WhatsApp phone-based ID
- **Secure Linking:** One-time tokens to connect WhatsApp → Web sessions

### Deployment
- **Docker Ready:** `docker-compose up -d` for quick deployment
- **NAS Optimized:** Runs efficiently on ASUSTOR/Synology/QNAP NAS devices
- **Optional Ngrok:** Public URL tunneling for WhatsApp webhooks

## Architecture

```
finance-assistant-bot/
├── chatbot_core.py          # Main NLP intent recognition engine
├── calculators.py           # Financial calculators (compound interest, payoff schedules)
├── visualizations.py        # Plotly chart generation
├── database.py              # SQLAlchemy models and session management
├── web_app.py               # Flask web server and API endpoints
├── templates/
│   └── chat.html            # Web chat interface
├── tests/                   # Comprehensive test suite
├── docs/
│   └── DEPLOY_NAS.md        # NAS deployment guide
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container definition
└── requirements.txt         # Python dependencies
```

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python web_app.py

# Access application
# Chat: http://localhost:5000/
# Dashboard: http://localhost:5000/dashboard
# Health Check: http://localhost:5000/health
```

### Docker Deployment
```bash
# Build and run containers
docker-compose up -d

# Verify health
curl http://localhost:5000/health

# View logs
docker-compose logs -f
```

### WhatsApp Integration (Optional)
1. **Set up Twilio:**
   - Configure webhook URL: `https://YOUR_DOMAIN/whatsapp-webhook`
   - Enable WhatsApp sandbox or production number

2. **Link WhatsApp to Web:**
   - Send "vincular" via WhatsApp
   - Receive one-time secure link
   - Open link to auto-login to web dashboard

3. **Use via WhatsApp:**
   - Send financial questions directly
   - Receive personalized advice and calculations
   - Access full conversation history on web

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web chat interface |
| POST | `/api/chat` | Process chat messages (JSON) |
| GET | `/dashboard` | Interactive financial dashboard |
| GET | `/health` | Health check endpoint |
| GET | `/api/user` | Get current user profile |
| POST | `/api/login` | Login (DNI or nickname) |
| POST | `/api/logout` | Logout current session |
| POST | `/whatsapp-webhook` | Twilio WhatsApp webhook |
| GET | `/claim/<token>` | Link WhatsApp to web session |

## Testing

Comprehensive test suite covering:
- Intent recognition accuracy
- Financial calculator correctness
- Context memory persistence
- API endpoint responses
- WhatsApp webhook handling

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Run specific test categories
pytest tests/test_chatbot_core.py -v
pytest tests/test_complex_v2_4.py -v

# Generate test report
python generate_test_report.py
```

## NAS Deployment

Optimized for home/office NAS deployment (ASUSTOR, Synology, QNAP):

1. **Transfer files to NAS:** Upload via SSH/SMB
2. **Install Docker:** Enable Container Manager on NAS
3. **Configure port:** Edit `docker-compose.yml` if port 5000 conflicts
4. **Deploy:** Run `docker-compose up -d`
5. **Optional Ngrok:** For WhatsApp integration, configure ngrok tunnel

See detailed guide: `docs/DEPLOY_NAS.md`

## Recent Improvements

- **Travel Intent → Savings:** "quiero viajar a…", "conocer/ir/visitar …" now route to savings calculators
- **Acronym Recognition:** CER/UVA/TNA/TEA/CFT trigger educational content; FCI/CEDEAR/ETF handled contextually
- **Context Retention:** Short replies ("24 meses", "si", numbers) maintain conversation flow
- **Slang Parsing:** Financial slang like "lucas" (thousands) correctly interpreted (e.g., "200 lucas" → 200,000)
- **Production Validation:** `/debug` endpoint shows deployment SHA1 and timestamps for version tracking

## Technologies Used

- **Python 3.12:** Core application language
- **Flask 2.3+:** Web framework and API
- **Twilio:** WhatsApp Business API integration
- **SQLite + SQLAlchemy:** Database and ORM
- **Plotly 5.18+:** Interactive data visualizations
- **Docker:** Containerization
- **Pytest:** Testing framework

## Documentation

- **`ESTRUCTURA_PROYECTO.md`:** Detailed project structure
- **`GUIA_DEMO.md`:** Demo presentation guide
- **`LOGS_ANALISIS.md`:** Log analysis and debugging
- **`docs/DEPLOY_NAS.md`:** NAS deployment instructions
- **`TIPS_PRESENTACION.md`:** Presentation tips for showcasing

## License

MIT License - See LICENSE file for details.

**Author:** Ramiro Ottone Villar  
**Portfolio Project:** Canadian Tech Market  
**Status:** Production-ready with Docker deployment
