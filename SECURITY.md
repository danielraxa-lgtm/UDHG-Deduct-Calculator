# Security Policy

## Reporting Security Issues

**Please do NOT open public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability in this project, please report it responsibly:

1. Email: **risk-management@udhg.com**
2. Include a description of the vulnerability and steps to reproduce
3. Allow reasonable time for the issue to be addressed before public disclosure

## Supported Versions

| Version | Supported |
|---------|-----------|
| Current (main branch) | Yes |

## Security Measures

This project implements the following security controls:

- Content Security Policy (CSP) headers via meta tags
- X-Frame-Options to prevent clickjacking
- X-Content-Type-Options to prevent MIME sniffing
- Referrer-Policy for privacy
- HTML output escaping to prevent XSS

## Known Limitations

- This is a static site hosted on GitHub Pages with no server-side backend
- Client-side authentication mechanisms (where used) are not a substitute for server-side security
- Sensitive operations should be performed through authenticated backend services

## Best Practices for Contributors

- Never commit API tokens, passwords, or secrets to the repository
- Never store credentials in client-side JavaScript
- Always escape user-supplied or API-sourced data before inserting into the DOM
- Use `textContent` instead of `innerHTML` where possible
- Report any exposed credentials immediately so they can be revoked
