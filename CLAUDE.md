# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static website for **Unified Door and Hardware Group (UDHG)** providing OCIP/CCIP (Owner Controlled Insurance Program / Contractor Controlled Insurance Program) information and insurance-related tools. The site serves as an internal resource for calculating insurance deductions during bid preparation and managing wrap-up insurance enrollments.

**Live Site:** https://structcor.github.io/UDHG-OCIP-CCIP/

## Project Structure

```
UDHG-OCIP-CCIP/
├── index.html              # Main hub page with tabbed interface
├── calculator.html         # Insurance cost worksheet calculator
├── formulas_and_rates.md   # Documentation for formulas and rates (placeholder)
├── CLAUDE.md               # AI assistant guidance (this file)
└── .github/
    └── workflows/
        └── static.yml      # GitHub Pages deployment workflow
```

## Technology Stack

- **Frontend**: Pure HTML, CSS, and JavaScript (no build tools or frameworks)
- **Styling**: Inline CSS within `<style>` tags in each HTML file
- **Fonts**: System font stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto...`)
- **Deployment**: GitHub Pages (auto-deploys from `main` branch)
- **No dependencies**: No npm, no build step, no external libraries

## Development Guidelines

### Code Style
- Use vanilla HTML/CSS/JavaScript only - no external dependencies
- Keep all styles inline within `<style>` tags in HTML files
- Keep all scripts inline within `<script>` tags at the bottom of HTML files
- Maintain responsive design using CSS media queries (primary breakpoint: 768px)

### Color Scheme
| Purpose | Color | Usage |
|---------|-------|-------|
| Primary Brand | `#8B2332` | Index page headers, buttons, accents |
| Calculator Primary | `#2c3e50` | Calculator headers, section titles |
| Confidential Banner | `#c0392b` | Warning banners |
| Success/Positive | `#27ae60` | O&P checkbox, email section |
| Warning | `#ffc107` / `#fff3cd` | Alert boxes, subcontractor section |
| Info Box | `#e8f4f8` | Information callouts |
| Background | `#f5f5f5` | Page background |

### Testing
- Open HTML files directly in a browser to preview changes
- Test responsive layouts at mobile (< 768px) and desktop (≥ 768px) breakpoints
- Verify calculator produces correct deduction amounts
- Test email generation functionality (mailto links)

### Deployment
- Push to `main` branch triggers automatic GitHub Pages deployment
- No build step required - files are served as-is
- Deployment is handled by `.github/workflows/static.yml`

## Key Features

### 1. Index Page (index.html)
Main hub with tabbed interface providing:
- **Process Flow tab**: Step-by-step OCIP/CCIP enrollment process, department responsibilities
- **Deduction Calculator link**: Opens calculator.html in new tab
- **COI Requests tab**: Certificate of Insurance request form with email generator
- **FAQ tab**: Common questions about wrap-up programs
- **Enrollment Info tab**: Contact information and enrollment requirements

Special features:
- SharePoint compatibility notice (dismissible)
- COI email generator with mailto link
- Contact information for Risk Management team

### 2. Calculator (calculator.html)
Insurance cost worksheet for bid preparation:
- **Project Information**: GC name, project details, state selection, contract value
- **Labor Scope Options**: None (delivery only), Subcontracted, Self-Performed
- **Insurance Calculations**:
  - Workers' Compensation (WC) - based on payroll and state rates
  - General Liability (GL) - based on contract value
  - Umbrella/Excess - based on contract value
  - Optional 15% Overhead & Profit markup
- **Email Integration**: Generate pre-formatted emails to Wrap Enrollment team

## Insurance Calculation Formulas

### Workers' Compensation (WC)
```
WC = (Payroll / 100) × Base Rate × EMR × Large Deductible Factor
```
- Only applies when labor scope is "Self-Performed"
- State-specific rates defined in `wcRates` object in calculator.html
- EMR (Experience Modification Rate) varies by state
- Large Deductible Factor provides credit in CT and RI

### General Liability (GL)
```
GL = (Contract Value / 1000) × 0.1506
```

### Umbrella/Excess
```
Umbrella = (Contract Value / 1000) × 0.36691
```

### Total Deduction
```
Subtotal = WC + GL + Umbrella
O&P (optional) = Subtotal × 0.15
Total = Subtotal + O&P
```

## State-Specific Data (Policy Year 2025-26)

The calculator includes state-specific rates for: AZ, CO, CT, FL, MA, MD, MI, NJ, NY, PA, RI, TX

Key data structures in calculator.html:
- `wcRates` - Base WC rates by state (Class Code 5102)
- `ldFactors` - Large Deductible Factors by state
- `emrFactors` - Experience Modification Rates by state
- `stateNames` - Full state names for email formatting

## Important Contacts

- **Wrap Enrollment Team**: wrap.enrollment@myfbm.com | 657-472-1661
- **Rose Picco** (Risk Management Admin): rose_picco@udhg.com
- **Daniel Raxa** (Director, Risk Management): daniel.raxa@myfbm.com
- **COI Requests**: SECertSpeed@lockton.com (CC: COI@myfbm.com)

## Important Notes

- **Confidential**: This is an internal business tool - do not distribute externally
- **Rate Updates**: Insurance rates change annually; verify rates match current policy year
- **Labor Cost vs Sell**: Always use labor COST (payroll) for WC calculations, not labor sell price
- **Accessibility**: Maintain accessibility standards for form inputs and navigation
- **Self-Install States**: UDHG approved for self-install in AZ, CO, FL, MD, MI, NJ, NY, PA, TX

## Common Tasks

### Updating Insurance Rates
1. Update `wcRates`, `emrFactors`, and `ldFactors` objects in calculator.html
2. Update the "Policy Year" reference in the footer
3. Verify calculations produce expected results

### Adding a New State
1. Add entry to `wcRates` with base rate
2. Add entry to `emrFactors` (use 1.0 if no modifier)
3. Add entry to `ldFactors` (use 1.0 if no large deductible)
4. Add entry to `stateNames` for email formatting
5. Add `<option>` to state dropdown in calculator.html

### Modifying Contact Information
- Index page: Update contact info in department boxes and contact boxes
- Calculator: Update email addresses in `emailWrapEnrollment()` function and contact box
