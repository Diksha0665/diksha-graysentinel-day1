# 🔐 Phishing Campaign Simulator

**Project 01 — GraySentinel Cyber Defence Lab, Sprint Day 1**
**Track:** Red Team (Offensive Security)
**Stack:** Python · Flask · SQLite · HTML · CSS · Jinja2

A controlled, local cybersecurity awareness training application that simulates a phishing campaign end-to-end — campaign creation, a fake-but-labeled email preview, click tracking, mock credential-submission detection, and a dashboard with an awareness-risk score.

> ⚠️ **Safety Notice:** This is strictly a training tool. It never sends real emails, never collects or stores real credentials, and never targets real people or infrastructure.

---

## 🎯 Why This Project

Phishing is consistently one of the top initial-access techniques behind real-world breaches — most attacks don't start with exploiting a server, they start with tricking a person into clicking a link or entering their credentials. Security teams counter this by running **phishing-awareness campaigns**: controlled, internal simulations that measure how many employees click a suspicious link or fall for a fake login page, so the organization can target training where it's actually needed.

This project was built to understand that workflow hands-on, from the Red Team side: how a campaign is structured, how a convincing-but-safe lure is presented, how interactions are tracked without violating user privacy or collecting real secrets, and how the results get turned into an actionable risk signal. Building it — rather than just reading about it — forces a real understanding of the full offensive-to-defensive loop: create the lure, track the interaction, measure the outcome, report the risk.

## 🎯 Objective

1. Create a simulated phishing campaign
2. Generate a realistic but clearly-labeled simulated email preview
3. Provide a controlled, local tracking link
4. Record simulated link-interaction events
5. Detect mock credential submissions without ever storing them
6. Display campaign statistics on a dashboard
7. Calculate a simple awareness-risk indicator (LOW / MEDIUM / HIGH)

---

## 🚀 Features

### 📧 Campaign Creation
Create a campaign with a name, email subject, and mock recipient name/email.

### 👀 Email Preview
A realistic-looking simulated phishing email, clearly marked as a training exercise, with a controlled verification link pointing only to the local app.

### 🔗 Simulated Click Tracking
Opening the tracking link logs an interaction event — timestamp, simulated IP (`127.0.0.1`), simulated location (`Localhost (simulated)`), and user-agent — to the database.

### 🔑 Mock Credential Submission
A mock login page demonstrates how a credential-submission event would be detected. Only the fact that a submission occurred is recorded (`credential_submitted = 1`) — no username or password is ever read or stored.

### 📊 Security Awareness Dashboard
Displays total sent, interactions, click rate, mock credentials, and per-campaign awareness-risk indicators.

### ⚠️ Awareness Risk Indicator

| Condition | Indicator |
|---|---|
| Mock credential submission detected | 🔴 HIGH |
| Click rate ≥ 30% | 🟠 MEDIUM |
| Lower interaction level | 🟢 LOW |

*(This is a training-awareness metric, not a production-grade risk score.)*

---

## 📁 Folder Structure

```
01-phishing-simulator/
│
├── src/
│   ├── app.py
│   └── database.py
│
├── static/
│   └── style.css
│
├── templates/
│   ├── dashboard.html
│   ├── campaign.html
│   ├── email_preview.html
│   └── simulation.html
│
├── phishing_simulator.db
├── README.md
├── report.md
└── .gitignore
```

---

## 🗄️ Database Design

**`campaigns`** — `id`, `name`, `subject`, `created_at`
**`recipients`** — `id`, `campaign_id`, `name`, `email`, `clicked`, `credential_submitted`
**`click_events`** — `id`, `recipient_id`, `clicked_at`, `ip_address`, `user_agent`, `location`

---

## 🔄 Application Workflow

```
Create Campaign
      │
      ▼
Email Preview
      │
      ▼
Simulated Verification Link
      │
      ▼
Click Event Recorded
      │
      ▼
Mock Verification Page
      │
      ▼
Mock Submission Event
      │
      ▼
Dashboard Updated
      │
      ▼
Awareness Risk Calculated
```

---

## ⚙️ Installation & Setup

```bash
# 1. Navigate to the project directory
cd 01-phishing-simulator

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\Activate.ps1      # PowerShell
venv\Scripts\activate          # Command Prompt

# 4. Install Flask
pip install flask
```

### Initialize the database
```bash
python src\database.py
```
Expected output: `Database initialized successfully.`

### Run the application
```bash
python src\app.py
```
Open the local address shown in the terminal, typically `http://127.0.0.1:5000`.

---

## 🧪 Testing Summary

| # | Test | Result |
|---|---|---|
| 1 | Campaign creation | ✅ Pass |
| 2 | Email preview rendering | ✅ Pass |
| 3 | Simulated click tracking | ✅ Pass |
| 4 | Mock credential submission (no password stored) | ✅ Pass |
| 5 | Dashboard metrics update | ✅ Pass |
| 6 | Risk indicator (LOW/MEDIUM/HIGH) | ✅ Pass |

Full methodology, results, and analysis are in [`report.md`](./report.md).

---

## 🔒 Security & Ethical Considerations

**Does NOT:**
- Send real phishing emails
- Collect or store real passwords
- Track real users or real locations
- Perform any action against real, unauthorized infrastructure

**Does:**
- Simulate phishing interactions locally
- Log local test events only
- Demonstrate security-awareness metrics and risk scoring
- Provide a local dashboard for analysis

## ⚠️ Limitations

1. No real email delivery — the flow starts at a local preview page, not an inbox.
2. IP/location values are simulated, not geolocated.
3. Risk scoring is rule-based, not statistically validated.
4. Single-user local SQLite database — not built for multi-tenant/production use.

---

## 🎓 Learning Outcomes

Flask web development · SQLite integration · HTTP GET/POST handling · URL-based interaction tracking · database CRUD operations · Jinja2 templating · HTML/CSS UI · event logging · security-awareness simulation · ethical, controlled testing methodology.

---

## 👨‍💻 Project Info

**Lab:** GraySentinel Cyber Defence Lab — Sprint Day 1
**Project:** Phishing Campaign Simulator
**Status:** ✅ Built • ✅ Tested • ✅ Documented
