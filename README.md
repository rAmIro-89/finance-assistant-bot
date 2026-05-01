# 💰 Finance Assistant 24/7

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Twilio-25D366?style=flat&logo=whatsapp&logoColor=white)](https://www.twilio.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**A deployable personal finance assistant chatbot for Spanish-speaking users, built with Flask, SQLite, Docker, web chat, and optional WhatsApp integration through Twilio.**

---

## 🎯 Problem Statement

Most financial education and planning tools are either:
- **Too complex** for everyday users (overwhelming features)
- **Too simplistic** (generic calculators without personalization)
- **Too expensive** (paid advisors, premium subscriptions)
- **Unavailable after hours** (fixed business hours)

**Finance Assistant 24/7** solves this by providing an intelligent, empathetic chatbot that:
- Guides users through real financial decisions in **natural language**
- **Validates input** and explains when decisions are unrealistic
- Suggests **actionable plans** with trade-offs and timelines
- Learns from **conversation history** to give better advice over time
- Logs all interactions for **compliance and analytics**

---

## ✨ Key Features

### 💳 **Budgeting Coach**
- Helps users structure income, expenses, and savings goals
- Suggests the **50/30/20 rule** (50% needs, 30% wants, 20% savings/debt)
- Provides actionable recommendations for expense reduction

### 📉 **Debt Payoff Planner**
- **Snowball Method** implementation: Pay smallest debts first for psychological wins
- User inputs total debt and monthly payment capacity
- Generates **3 customized payoff plans** (6 / 12 / 18 months) with realistic timelines and interest impact
- **Input validation** with clear warnings (e.g., "You must pay at least $X/month to reach your goal")
- Shows visualization of interest vs. principal over time

### 📈 **Investment Suggestions**
- Asks user for investment amount and time horizon
- Recommends **diversified portfolios** for moderate risk profiles:
  - Global ETFs (VOO, VGRO, SPLG, etc.)
  - Balanced mutual funds
  - Regional stocks (CEDEARs, ADRs)
  - Fixed income options
- **Compound interest simulator** to show long-term growth potential
- Risk profile assessment (Conservative / Moderate / Aggressive)

### 🧮 **Financial Calculator**
- **Compound Interest**: "If I invest X at Y% for N years, how much will I have?"
- **Loan Payment**: "What's my monthly payment for X over N months at Y%?"
- **Payoff Timeline**: "How long to pay X debt if I pay Y monthly?"
- **Investment Comparison**: Side-by-side analysis of multiple scenarios
- Real-time results with clear formatting

### 📚 **Financial Education & Tips**
- Short, digestible explanations of key concepts:
  - Snowball vs. Avalanche (debt payoff methods)
  - Portfolio diversification and asset allocation
  - Compound interest and the power of early investing
  - Emergency fund sizing
- **Practical, actionable advice**:
  - Budget-cutting strategies
  - Negotiation tips for rates and fees
  - Side income ideas
  - Credit score improvement tactics

### 📊 **Dashboard & Analytics**
- Stores all user interactions in SQLite database
- Real-time conversation logs with timestamp, sentiment, and classification
- Analytics dashboard showing:
  - **Topic distribution** (budgets, investments, debt, education)
  - **Sentiment trends** (positive, neutral, negative)
  - **User engagement metrics** (frequency, session length)
  - **Most common questions** and use cases
- Export-ready data for further analysis

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────┐
│   Users (WhatsApp / Web Chat)   │
└────────────┬────────────────────┘
             │
      ┌──────▼──────┐
      │   Twilio    │
      │ + Frontend  │
      └──────┬──────┘
             │
   ┌─────────▼────────────┐
   │  Flask REST API      │
   │ (Finance Assistant   │
   │     Core Engine)     │
   └─────────┬────────────┘
             │
    ┌────────┴────────┐
    │                 │
 ┌──▼──┐      ┌──────▼──────┐
 │SQLite│      │  Analytics  │
 │ DB   │      │ Dashboard   │
 │Logs  │      │ (Plotly UI) │
 └──────┘      └─────────────┘
```

### **Stack**
- **Backend**: Python 3.9+ | Flask 2.3+ | SQLAlchemy ORM
- **Messaging**: Twilio WhatsApp API + Web Chat Frontend (HTML/JS)
- **Database**: SQLite (dev) | Can scale to PostgreSQL (production)
- **Analytics**: Plotly for interactive charts | Custom Plotly dashboards
- **Deployment**: Docker containerization | Environment-based config
- **Logging & Monitoring**: Custom CSV logs | Dashboard analytics

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.9+
- Twilio account (for WhatsApp integration) — *optional for web-only mode*
- Docker (optional, for containerized deployment)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/rAmIro-89/finance-assistant-bot.git
   cd finance-assistant-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (create `.env` file)
   ```bash
   FLASK_ENV=development
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   DATABASE_URL=sqlite:///finance_assistant.db
   ```

### **Run the Application**

**Web Chat Mode** (local development):
```bash
python web_app.py
# Open http://localhost:5000 in your browser
```

**WhatsApp Integration** (requires Twilio):
1. Set up Twilio webhook to point to `https://your-domain/whatsapp-webhook`
2. Test in Twilio sandbox: Send a message to get started

**Docker Deployment**:
```bash
docker-compose up --build
# App runs on http://localhost:5000
```

### **View Analytics Dashboard**
```bash
python web_app.py
# Navigate to http://localhost:5000/dashboard
```

---

## 📸 Screenshots

### Welcome Screen & Main Capabilities
![Home screen – Finance Assistant 24/7](img/01-home-intro.jpg)

### Debt Payoff Planner Flow
![Debt planner conversation flow](img/02-debt-flow.jpg)

### Extreme Case Example – Unrealistic Payment Plan
![Extreme payoff example – 150000 debt, 1 per month](img/03-debt-extreme-case.jpg)

### Investment Recommendations
![Investment options for a moderate risk profile](img/04-investments.jpg)

### Financial Calculator Menu
![Financial calculator menu](img/05-calculator.jpg)

### Analytics Dashboard
![Dashboard – User interactions, sentiment analysis, topic distribution](img/06-dashboard.jpg)

---

## 📁 Project Structure

```
finance-assistant-bot/
├── web_app.py              # Flask API + web routes
├── chatbot_core.py         # Core NLP + conversation logic
├── database.py             # SQLAlchemy models & persistence
├── calculators.py          # Financial calculators (compound interest, etc.)
├── visualizations.py       # Plotly chart generation
├── chat.html               # Web chat frontend
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container setup
├── docker-compose.yml      # Multi-container orchestration
├── .env.example            # Template for environment variables
├── tests/                  # Unit & integration tests
│   ├── test_chatbot_core.py
│   ├── test_calculators.py
│   └── test_flows.py
├── src/                    # Organized Python modules (optional)
│   ├── __init__.py
│   └── utils/              # Helper functions
├── data/                   # Logs and data files
│   ├── chat_logs.csv
│   └── processed/
├── img/                    # Screenshots & diagrams
├── docs/                   # Additional documentation
│   ├── API_REFERENCE.md
│   ├── CONVERSATION_FLOWS.md
│   └── DEPLOYMENT.md
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## 🔌 API Endpoints

### **Chat Endpoint**
```
POST /api/chat
Content-Type: application/json

{
  "message": "I want to pay off my debt",
  "when": "15:30"  # Optional: override current time
}

Response:
{
  "reply": "Great! How much total debt are you carrying?",
  "scenario": "deudas",
  "timestamp": "2025-12-04T15:30:00",
  "sentiment": "positivo",
  "emotion": "hopeful"
}
```

### **User Profile Endpoint**
```
GET /api/user
Response:
{
  "exists": true,
  "name": "John",
  "phone": "nickname_user",
  "monthly_income": 50000,
  "total_debt": 0,
  "current_savings": 0,
  "risk_profile": "moderate"
}
```

### **Dashboard Endpoints**
```
GET /dashboard         # Full interactive dashboard
GET /logs              # Conversation logs table with filters
GET /api/grafico/presupuesto?ingreso=50000   # Budget chart
GET /api/grafico/inversion?capital=10000&tasa=12&años=5   # Investment chart
GET /api/grafico/comparacion?monto=100000&años=10         # Comparison chart
```

---

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Example test coverage:
- **Conversation flows**: Debt payoff, investments, budgeting
- **Input validation**: Edge cases (zero payments, negative amounts)
- **Calculator accuracy**: Compound interest, loan payments
- **Database persistence**: User state and conversation history
- **WhatsApp integration**: Webhook message handling

---

## 📊 Technologies & Dependencies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Flask 2.3+ | REST API & web routing |
| **NLP** | spaCy, NLTK | Sentiment analysis & intent classification |
| **Database** | SQLAlchemy + SQLite | User profiles, logs, conversation history |
| **Messaging** | Twilio | WhatsApp integration |
| **Analytics** | Plotly | Interactive dashboards |
| **Frontend** | HTML/CSS/JS | Web chat interface |
| **Container** | Docker | Reproducible deployment |
| **Testing** | pytest | Automated test suite |

Full dependencies in [`requirements.txt`](requirements.txt)

---

## 🚀 Deployment

### **Local Development**
```bash
python web_app.py
# Runs on http://localhost:5000
```

### **Docker**
```bash
docker-compose up -d
# Access at http://localhost:5000
# All logs written to container stdout
```

### **Production (Cloud)**
- Deploy container to **AWS ECS / Heroku / Google Cloud Run**
- Use **PostgreSQL** instead of SQLite for concurrency
- Enable **HTTPS** for Twilio webhooks
- Set up **monitoring** (CloudWatch, Sentry, New Relic)
- Configure **auto-scaling** based on traffic

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for detailed instructions.

---

## 💡 Real-World Example

**Scenario**: User has $150,000 debt but can only pay $1/month

**Bot behavior**:
1. User enters: "I have 150,000 debt and can pay 1 per month"
2. Bot calculates: 150,000 months = ~12,500 years 😱
3. **Validation trigger**: "At $1/month, it would take 12,500 years. That's unrealistic!"
4. Bot suggests: "Try $500/month (125 months), $1000/month (75 months), or $2000/month (50 months)"
5. Shows interest impact for each option
6. User picks $500/month, bot creates a payment schedule

This **demonstrates**:
- Natural language understanding
- Financial literacy (not just computation)
- Empathy (acknowledges the struggle)
- Practical guidance (realistic alternatives)

---

## 🔐 Security & Privacy

- **No third-party financial data**: All calculations are client-side
- **No credit score checks or API calls**: User data stays local
- **Encrypted conversations** (in production, use HTTPS)
- **SQLite encryption** option for sensitive data
- **GDPR-compliant**: Users can request data export or deletion
- **Twilio compliance**: Follows WhatsApp Business API terms

---

## 📈 Analytics Capabilities

The dashboard provides insights into:
- **Conversation volume** by topic and date range
- **Sentiment trends** (positive feedback, concerns, frustration)
- **Most common questions** (budgeting, debt payoff, investments)
- **User engagement metrics** (repeat users, session duration)
- **Feature popularity** (which calculators are used most)
- **Conversation quality** (response relevance, user satisfaction)

Use these insights to:
- Improve conversational responses
- Add new features based on user demand
- Identify pain points in debt management
- Optimize investment recommendations

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Enhanced NLP for intent classification
- Additional calculators (tax optimization, insurance planning)
- Multi-language support (Spanish, Portuguese, French)
- Integration with external financial APIs
- Mobile app wrapper
- Machine learning for personalized advice

---

## 📞 Support & Feedback

For questions or feedback:
- Open an **Issue** on GitHub
- Contact: See GitHub profile

---

## 📝 License

MIT License — free to use, modify, and distribute. See [`LICENSE`](LICENSE) for details.

---

## 👤 Author

**Ramiro Ottone Villar**

[![GitHub](https://img.shields.io/badge/GitHub-rAmIro--89-181717?style=flat&logo=github)](https://github.com/rAmIro-89)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/ramiro-ottone-villar)

---

*Built for Spanish-speaking users who deserve accessible, empathetic financial guidance, 24/7.*
