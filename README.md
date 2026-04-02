# Datadog Monitor as Code — DCE Pilot

This repository contains scripts and documentation for the Monitor as Code (MaC)
initiative focused on the Digital and Commercial Engineering (DCE) pillar under
the GCC L1 team.

## Background

Datadog monitors for the DCE pillar are currently created and managed manually
through the UI. There is no version control, no review process, and no audit
trail for changes. This initiative introduces Monitor as Code using Terraform to
bring the full monitor lifecycle under version control.

This repo covers the end-to-end pilot: discovery and audit → technical design →
Terraform pilot migration → SOP → outcome.

---

## Repository Structure

```
datadog-mac-initiative/
├── scripts/
│   ├── extract_dce_monitors.py   # Extracts DCE L1 monitors via Datadog API
│   └── audit_dce_monitors.py     # Processes raw data into audit spreadsheet
├── docs/
│   ├── images/
│   │   └── 01-discovery/         # Evidence screenshots from audit phase
│   └── ...                       # Design docs and SOPs (added progressively)
├── data/                         # Generated outputs - not committed (see .gitignore)
├── .env.example                  # Template for required environment variables
├── .gitignore
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-org/datadog-mac-initiative.git
cd datadog-mac-initiative
```

### 2. Install dependencies

```bash
pip install requests python-dotenv openpyxl
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```
DD_API_KEY=your_datadog_api_key
DD_APP_KEY=your_datadog_application_key
```

> **Never commit your `.env` file.** It is listed in `.gitignore`.

---

## Usage

### Step 1 — Extract DCE monitors

```bash
python scripts/extract_dce_monitors.py
```

Saves `data/dce_monitors_raw.json` with all 404 DCE L1 monitors.

### Step 2 — Generate audit spreadsheet

```bash
python scripts/audit_dce_monitors.py
```

Saves `data/dce_monitor_audit.xlsx` with two sheets:

- **Monitor Audit** — every monitor with colour-coded recommendations
- **Summary** — totals by status, recommendation, SNOW routing, and tag gaps

---

## Key Findings (Discovery Phase)

| Finding                | Count      | Impact                              |
| ---------------------- | ---------- | ----------------------------------- |
| Total DCE L1 monitors  | 404        | Full scope                          |
| No Data status         | 101 (25%)  | Active monitoring blind spots       |
| Muted monitors         | 43 (10.6%) | Silenced with no audit trail        |
| L2 Direct SNOW routing | 21         | Potential ownership gaps            |
| Unknown SNOW routing   | 4          | Needs investigation                 |
| No SNOW integration    | 2          | Alerts fire but no incident created |
| Ready to Migrate       | 285 (70%)  | Terraform pilot candidates          |

---

## Initiative Phases

- [x] Phase 1 — Discovery & Audit
- [ ] Phase 2 — Technical Design & SOP
- [ ] Phase 3 — Pilot Migration (Terraform)
- [ ] Phase 4 — CI/CD Pipeline
- [ ] Phase 5 — Outcome & Stakeholder Reporting

---

## Related

- Azure DevOps Epic: `Monitor as Code (MaC) — DCE Pillar Pilot`
- Datadog Org: `tr-digital-prod.datadoghq.com`
- API Base URL: `https://api.datadoghq.com`
