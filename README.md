# UDHG OCIP/CCIP Risk Management Portal

## 🎯 Overview

Comprehensive web-based platform for managing Owner Controlled Insurance Programs (OCIP) and Contractor Controlled Insurance Programs (CCIP) for Unified Door and Hardware Group.

## ✨ Features

### 📊 Live Dashboard
- Real-time compliance monitoring across all programs
- Financial impact tracking with bid deduct analysis
- Automated alert system for deadlines and compliance issues
- Visual compliance scoring with color-coded indicators

### 🔧 Tools & Automation
- **Compliance Reporter**: Automated weekly/monthly reporting
- **Data Sync Engine**: Real-time synchronization with backend systems
- **Insurance Calculator**: Bid deduct and cost analysis tools
- **Bond Management**: Secure tracking of pending bonds and requests

### 🛡️ Security
- Password-protected access to sensitive bond data
- Confidential business information handling
- SHA-256 encrypted authentication

## 🏗️ Architecture

```
UDHG-OCIP-CCIP/
├── index.html              # Main hub with navigation
├── dashboard.html           # Live monitoring dashboard  
├── calculator.html          # Insurance cost calculator
├── ocip_ccip.html          # Program details and enrollment
├── pending_bonds.html       # Secure bond tracking
├── api/                     # Real-time data endpoints
│   ├── wrapup-status.json  # Dashboard data feed
│   └── programs/           # Individual program details
└── tools/                  # Backend automation
    ├── compliance-reporter.py  # Automated reporting
    └── data-sync.py           # Real-time data sync
```

## 🚀 Recent Enhancements (Feb 2026)

### Live Dashboard System
- Added real-time compliance monitoring
- Automated alert generation for deadline management
- Financial impact visualization
- Multi-program status tracking

### Backend Integration  
- Database synchronization with wrap-up manager systems
- Automated compliance scoring algorithms
- Real-time deadline monitoring
- Financial metrics calculation

### Reporting Automation
- Weekly compliance reports
- Deadline check automation  
- Financial impact analysis
- Management-ready summary generation

## 💰 Value Proposition

### Cost Savings
- **$452,650** in estimated annual savings across active programs
- **64% average compliance** reduces penalty risk
- **Automated monitoring** eliminates manual tracking overhead
- **Early deadline alerts** prevent costly missed submissions

### Risk Mitigation
- Real-time compliance monitoring prevents gaps
- Automated deadline tracking reduces human error
- Consistent documentation ensures program requirements are met
- Financial tracking optimizes bid deduct strategies

### Operational Efficiency
- **Centralized portal** eliminates spreadsheet chaos
- **Automated reports** save 4-6 hours weekly
- **Real-time alerts** enable proactive management
- **Self-service access** reduces coordination overhead

## 🔄 Integration

### Current Systems
- **Origami RMIS**: Incident tracking and routing
- **Wrap-Up Manager Database**: Compliance and enrollment data
- **Email Systems**: Automated deadline notifications
- **Financial Systems**: Contract value and savings tracking

### API Endpoints
```
GET /api/wrapup-status.json       # Dashboard data
GET /api/programs/{id}.json       # Program details
```

## 📈 Metrics (Current Period)

- **4 Active Programs** being monitored
- **$11.8M Total Contract Value** under management  
- **3.9% Average Bid Deduct** across programs
- **85% On-time Compliance** for payroll reporting
- **<24hr Alert Response** time for critical deadlines

## 🛠️ Technical Stack

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Backend**: Python automation tools
- **Database**: SQLite with real-time sync
- **Hosting**: GitHub Pages with API integration
- **Security**: SHA-256 authentication, confidential data handling

## 📞 Support

For technical issues or feature requests, contact the Risk Management automation team.

---
*Last Updated: February 27, 2026*  
*Status: Production Ready*