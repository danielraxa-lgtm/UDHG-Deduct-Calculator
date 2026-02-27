# UDHG OCIP/CCIP Risk Management Portal — Proof of Concept

## What This Is

This is a working blueprint for a centralized OCIP/CCIP management portal built for Unified Door and Hardware Group. It's designed to show what's possible — not to replace any production systems today.

The portal was built to demonstrate how we could consolidate wrap-up program tracking, compliance monitoring, and bid deduction tools into one place instead of scattered spreadsheets and manual processes.

**Important: This is a proof of concept.** All project data currently shown in the dashboard is sample data for demonstration purposes. No live project information is being stored or saved at this time. The dashboard is showing you that this type of data *can* be captured and displayed — it's not reflecting real program activity yet.

---

## What's Been Built So Far

### Live Dashboard (Sample Data)
- Real-time compliance monitoring layout across programs
- Financial impact tracking with bid deduct analysis
- Automated alert system for deadlines and compliance issues
- Visual compliance scoring with color-coded indicators

*All dashboard data is placeholder/test data to demonstrate the capability.*

### Insurance Calculator
- Bid deduct and cost analysis tools matching our current OCIP/CCIP deduction logic
- State-specific workers' comp rates, GL, and umbrella calculations

### Program Management Pages
- OCIP/CCIP program details and enrollment reference
- Bond tracking with basic password protection

### Backend Automation (Early Stage)
- Compliance reporting scripts (Python)
- Data sync engine for database integration
- SQLite database structure for storing program data

---

## What This Could Do at Scale

If we decide to move forward with this, the portal could:

- Replace manual spreadsheet tracking for all wrap-up projects
- Automate compliance deadline alerts so nothing slips through the cracks
- Give management a single view of all active programs, savings, and risk exposure
- Generate reports without someone having to pull data from five different places
- Track actual payroll reporting compliance and enrollment status in real time

### Estimated Impact (Based on Current Program Volume)
- Potential to save 4-6 hours weekly on manual tracking and reporting
- Centralized data reduces errors from outdated or conflicting spreadsheets
- Proactive deadline monitoring vs. reactive catch-up

---

## Current Limitations — What Would Need to Happen Next

This is hosted on GitHub Pages, which is essentially bare-bones HTML/CSS/JavaScript. It works fine for a proof of concept, but for actual production use:

- **IT would need to be involved.** Enterprise security protocols, authentication, and access controls would need to be implemented. I put some basic security in place (SHA-256 password hashing for the bond page), but that's nowhere near what IT would require for handling real project and financial data.
- **Database infrastructure.** Right now the backend uses SQLite, which is lightweight and good for prototyping. A production version would likely need a more robust database solution, managed by IT.
- **Hosting.** GitHub Pages is fine for demos. A real deployment would need to live on company infrastructure or an approved cloud environment.
- **Data integration.** Connecting to Origami RMIS, wrap-up manager systems, and payroll would require IT coordination and proper API development.

---

## Architecture

```
UDHG-OCIP-CCIP/
├── index.html              # Main hub with navigation
├── dashboard.html           # Live monitoring dashboard (SAMPLE DATA)
├── calculator.html          # Insurance cost calculator
├── ocip_ccip.html          # Program details and enrollment
├── pending_bonds.html       # Bond tracking (basic auth)
├── api/                     # Data endpoints (test data)
│   ├── wrapup-status.json
│   └── programs/
└── tools/                  # Backend automation scripts
    ├── compliance-reporter.py
    └── data-sync.py
```

## Technical Stack
- Frontend: HTML/CSS/JavaScript (no frameworks)
- Backend: Python automation tools
- Database: SQLite (prototype)
- Hosting: GitHub Pages
- Security: Basic (SHA-256 auth on sensitive pages)

---

## Bottom Line

This is here to show what we could build — not what's in production. Think of it as the blueprint. Everything you see can be edited, expanded, or scaled as needed. If leadership wants to move forward, the next step would be bringing IT in to evaluate the concept and build it out with proper enterprise infrastructure.
*Status: Production Ready*
