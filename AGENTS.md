# AGENTS.md

Guidance for coding agents working in this repository.

## Project Summary

This repository hosts a static internal website for Unified Door and Hardware Group (UDHG) focused on OCIP/CCIP insurance information and a cost worksheet calculator.

## Tech Stack

- Plain HTML, CSS, and JavaScript
- No framework, no build step
- GitHub Pages static hosting

## Repository Layout

- `index.html`: Main informational hub with tabbed OCIP/CCIP content
- `calculator.html`: Insurance worksheet calculator logic and UI
- `formulas_and_rates.md`: Formula and rate documentation
- `.github/workflows/static.yml`: GitHub Pages deployment workflow

## Editing Rules

1. Use vanilla HTML/CSS/JS only; avoid introducing external dependencies.
2. Keep CSS inline in each HTML file inside `<style>` tags.
3. Preserve responsive behavior; validate at mobile (`< 768px`) and desktop widths.
4. Keep branding consistent with maroon `#8B2332` where existing design uses it.
5. Maintain semantic HTML and accessible labels/controls.
6. Treat business content as confidential and avoid unnecessary wording changes.

## Calculator Safety Checks

When changing `calculator.html`:

- Preserve existing insurance math behavior unless explicitly requested.
- Keep field names/inputs aligned with current worksheet flow.
- Cross-check formulas against `formulas_and_rates.md`.

## Validation Checklist

- Open changed HTML files in a browser.
- Confirm layout and readability on mobile and desktop.
- Verify calculator inputs/outputs and totals still compute as expected.
- Ensure no broken links between `index.html` and `calculator.html`.

## Deployment Notes

- Site is served as static files.
- Pushing to the main deployment branch triggers GitHub Pages workflow.
