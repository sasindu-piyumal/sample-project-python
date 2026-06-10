# Security Policy

## Reporting a Vulnerability

This project takes security seriously and welcomes responsible disclosure of vulnerabilities. If you discover a security vulnerability in llm-benchmarking-py, please report it responsibly following the guidelines below.

### How to Report

Please **do not** create public GitHub issues for security vulnerabilities. Instead, report security concerns to:

**Email:** [security@turintech.ai](mailto:security@turintech.ai)

When reporting a vulnerability, please include:

- **Vulnerability Description:** A clear and detailed description of the vulnerability
- **Affected Versions:** Which version(s) of llm-benchmarking-py are affected
- **Reproduction Steps:** Step-by-step instructions to reproduce the issue (if applicable)
- **Impact Assessment:** The potential impact of the vulnerability (e.g., data exposure, code execution, denial of service)
- **Suggested Fix:** If you have identified a fix, please include it (optional but helpful)
- **Your Contact Information:** Name, email, and optionally an organizational affiliation

### What NOT to Do

- **Do not** disclose the vulnerability publicly before we have had a reasonable opportunity to address it
- **Do not** test vulnerabilities on any systems without explicit permission
- **Do not** access, modify, or delete data other than what is necessary to demonstrate the vulnerability
- **Do not** create public issues, pull requests, or commits related to the vulnerability

## Response Timeline

We are committed to responding to security reports in a timely manner:

- **Initial Response:** We will acknowledge receipt of your report within **48 hours**
- **Assessment & Communication:** We will provide initial assessment of the report within **5 business days**
- **Fix Development:** We aim to develop and test a fix within **30 days** of report confirmation
- **Release & Disclosure:** Security patches will be released as soon as they are ready, followed by coordinated disclosure

## Scope

This project is an algorithmic benchmarking library for LLM projects. Our security focus includes:

### In Scope

- Packaging and distribution vulnerabilities
- Dependency supply chain risks (malicious or compromised dependencies)
- Code vulnerabilities affecting installation or runtime execution
- Data handling vulnerabilities in the benchmarking functions
- Configuration or secrets exposure risks

### Out of Scope

- Vulnerabilities in third-party libraries (please report directly to the maintainers of those projects)
- Social engineering attacks
- Vulnerabilities in CI/CD infrastructure (except as they affect the released package)
- Vulnerabilities requiring significant infrastructure changes or policy modifications
- Security concerns in user code or configurations external to this library

## Security Best Practices

When using llm-benchmarking-py:

- **Keep Dependencies Updated:** Regularly update this library and its dependencies to receive security patches
- **Use Version Pinning:** Pin versions in production environments and update thoughtfully
- **Report Upstream Issues:** If you find vulnerabilities in our dependencies, report them to the respective maintainers
- **Review Pull Requests:** Be cautious when reviewing and merging pull requests from untrusted sources

## Responsible Disclosure & Acknowledgment

We believe in responsible disclosure and appreciate the work of security researchers. If you report a vulnerability:

- **Credit:** We will credit you publicly (with your permission) in security advisories and release notes
- **Timeline:** Please allow a reasonable time for us to develop and deploy fixes before public disclosure
- **Coordination:** We are happy to coordinate the timing of your disclosure with our patch release if desired
- **Opt-Out:** If you prefer not to be credited, please let us know when submitting your report

## Supported Versions

Security updates are provided for:

- **Current Version:** Latest released version receives all security patches
- **Previous Version:** The previous major/minor version receives critical security patches
- **Older Versions:** Users are encouraged to upgrade to the latest version

| Version | Status | Security Updates |
|---------|--------|------------------|
| 0.1.x   | Current | Yes |
| < 0.1   | Obsolete | No |

## Contact Information

For security-related inquiries:

- **Security Email:** [security@turintech.ai](mailto:security@turintech.ai)
- **Response Time:** Expect an initial response within 48 hours during business hours

## Additional Resources

- [OWASP - Responsible Disclosure](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/00-Foreword_and_Guidance/README)
- [HackerOne - Vulnerability Disclosure Best Practices](https://www.hackerone.com/disclosure-guidelines)
- [Python Security Advisory Database](https://pypa.io/en/latest/)

## Changes to This Policy

This security policy may be updated from time to time. We will notify relevant parties of any significant changes. The most current version is always available in the project repository.

Last Updated: 2024
