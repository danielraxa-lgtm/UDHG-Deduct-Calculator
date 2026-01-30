# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static website for **Unified Door and Hardware Group (UDHG)** providing OCIP/CCIP (Owner Controlled Insurance Program / Contractor Controlled Insurance Program) information and insurance-related tools.

## Project Structure

```
UDHG-OCIP-CCIP/
├── index.html           # Main hub page with tabbed interface for OCIP/CCIP info
├── calculator.html      # Insurance cost worksheet calculator
├── formulas_and_rates.md # Documentation for formulas and rates
└── .github/
    └── workflows/
        └── static.yml   # GitHub Pages deployment workflow
```

## Technology Stack

- **Frontend**: Pure HTML, CSS, and JavaScript (no build tools or frameworks)
- **Styling**: Inline CSS with responsive design
- **Deployment**: GitHub Pages (auto-deploys from `main` branch)

## Development Guidelines

### Code Style
- Use vanilla HTML/CSS/JavaScript - no external dependencies
- Keep all styles inline within `<style>` tags in the HTML files
- Maintain responsive design using CSS media queries
- Follow the existing color scheme (maroon `#8B2332` for branding elements)

### Testing
- Open HTML files directly in a browser to preview changes
- Test responsive layouts at mobile (< 768px) and desktop breakpoints

### Deployment
- Push to `main` branch triggers automatic GitHub Pages deployment
- No build step required - files are served as-is

## Key Features

1. **Index Page (index.html)**: Tabbed interface covering:
   - OCIP/CCIP program overview and enrollment process
   - Insurance requirements and documentation
   - Safety guidelines and compliance

2. **Calculator (calculator.html)**: Insurance cost worksheet for calculating:
   - Workers' compensation costs
   - General liability costs
   - Credit calculations based on insurance rates

## Important Notes

- This is an internal business tool - treat content as confidential
- Calculator formulas should match industry-standard insurance calculations
- Maintain accessibility standards for form inputs and navigation
