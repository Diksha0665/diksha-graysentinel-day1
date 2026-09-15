# 📄 Project Report — Phishing Campaign Simulator

**Project:** 01-phishing-simulator
**Lab:** GraySentinel Cyber Defence Lab — Sprint Day 1
**Track:** Red Team (Offensive Security)
**Technology Stack:** Python, Flask, SQLite, HTML, CSS, Jinja2

---

## 1. Introduction

Phishing remains one of the most common initial-access techniques used in real-world cyberattacks, and organizations regularly run controlled phishing-awareness campaigns to measure and improve employee resilience against them. This project implements a **safe, local simulation** of that workflow — allowing a campaign to be created, a simulated phishing email to be previewed, interactions to be tracked, and awareness metrics to be calculated — without ever sending a real email, contacting a real user, or storing a real credential.

## 2. Objective

The objective of this project was to understand and reproduce the core mechanics of a phishing-awareness campaign, specifically:

1. Creating a simulated phishing campaign
2. Generating a realistic but clearly-labeled simulated email preview
3. Providing a controlled, local tracking link
4. Recording simulated link-interaction events
5. Detecting mock credential submissions without storing them
6. Presenting campaign statistics on a dashboard
7. Calculating a simple awareness-risk indicator (LOW / MEDIUM / HIGH)

## 3. Methodology

The project was built incrementally as a Flask web application backed by a local SQLite database:

- **Backend:** Flask routes handle campaign creation, email preview rendering, click-tracking, and mock-submission handling.
- **Database:** SQLite stores three related tables — `campaigns`, `recipients`, and `click_events` — connected via foreign keys, allowing per-campaign statistics to be aggregated.
- **Frontend:** Each page (`dashboard.html`, `campaign.html`, `email_preview.html`, `simulation.html`) was built with Jinja2 templating and a shared `style.css`, giving the app a consistent "GraySentinel" branded interface with a navbar, status indicators, and card-based layouts.
- **Testing:** Each feature was manually tested end-to-end and screenshotted as proof of functionality.

## 4. Implementation

### 4.1 Campaign Creation
A form collects a campaign name, email subject, and mock recipient name/email, which are written to the `campaigns` and `recipients` tables.

### 4.2 Email Preview
The `email_preview.html` route renders a realistic phishing-style email — subject, sender framing, and a call-to-action button — clearly labeled with a training banner (**"⚠️ TRAINING SIMULATION — This is not a real email."**) and a verification button that links only to the local simulation route.

### 4.3 Click Tracking
Opening the tracking link logs an interaction event to the `click_events` table, capturing a timestamp, a simulated IP (`127.0.0.1`), a simulated location (`Localhost (simulated)`), and the browser's user-agent string.

### 4.4 Mock Credential Submission
The `simulation.html` page presents a mock login form. On submission, the app records only a boolean flag (`credential_submitted = 1`) — the actual username/password values entered are never read into memory or written to the database.

### 4.5 Dashboard & Risk Indicator
The dashboard aggregates totals (sent, interactions, click rate, mock credentials) per campaign and assigns an awareness-risk label:

| Condition | Indicator |
|---|---|
| Mock credential submission detected | 🔴 HIGH |
| Click rate ≥ 30% | 🟠 MEDIUM |
| Lower interaction level | 🟢 LOW |

## 5. Database Design

**`campaigns`** — `id`, `name`, `subject`, `created_at`
**`recipients`** — `id`, `campaign_id`, `name`, `email`, `clicked`, `credential_submitted`
**`click_events`** — `id`, `recipient_id`, `clicked_at`, `ip_address`, `user_agent`, `location`

## 6. Testing & Results

The application was tested manually end-to-end across six scenarios, each verified successful and documented with a screenshot:

| # | Test | Expected Result | Outcome |
|---|---|---|---|
| 1 | Campaign creation | Campaign appears in dashboard | ✅ Pass |
| 2 | Email preview | Simulated email renders with tracking link | ✅ Pass |
| 3 | Simulated click | Click event recorded in DB | ✅ Pass |
| 4 | Mock credential submission | Submission flagged, no password stored | ✅ Pass |
| 5 | Dashboard metrics | Totals/click rate update correctly | ✅ Pass |
| 6 | Risk indicator | Correct LOW/MEDIUM/HIGH label shown | ✅ Pass |

*(See `screenshots/` for step-by-step visual proof of each test.)*

## 7. Risk Assessment

The awareness-risk indicator is intentionally simple — a rule-based classification derived from click rate and credential-submission status, rather than a statistical or ML-based scoring model. It is designed purely as a **training illustration** of how real awareness platforms surface campaign risk, not as a production-grade metric.

## 8. Security Considerations

- No real emails are sent — the "email" is a rendered local HTML page only.
- No real credentials are ever read, logged, or persisted.
- IP address and location values are hardcoded/simulated, not collected from real network requests.
- All data lives in a local SQLite file with no external network exposure.
- The project is intended solely for supervised, local, educational use.

## 9. Limitations

1. No real email delivery — the flow starts from a local preview page, not an inbox.
2. Local-only telemetry — IP/location are simulated, not geolocated.
3. Simplified risk model — rule-based, not adaptive or statistically validated.
4. Single-user, local database — not designed for multi-tenant or production deployment.

## 10. Conclusion

This project demonstrates a working, end-to-end simulation of a phishing-awareness campaign — from campaign creation through email preview, interaction tracking, mock credential-submission detection, and risk-based reporting — built entirely with Flask and SQLite. It reinforces core web-application security concepts (event logging, safe handling of sensitive input, and awareness metrics) while strictly avoiding any real-world data collection or real phishing activity.

---

**Status:** ✅ Built • ✅ Tested • ✅ Documented
