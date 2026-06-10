# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it responsibly by emailing security concerns to the project maintainers rather than disclosing them publicly.

Please include the following information in your report:
- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any suggested remediation

We will acknowledge receipt of your report within 5 business days and will keep you updated on the progress toward fixing the issue.

## Supported Versions

We provide security updates for the latest release. Users are encouraged to upgrade to the latest version to receive security patches and improvements.

| Version | Status          |
|---------|-----------------|
| latest  | Supported       |
| < 0.1.0 | Not Supported   |

## Security Best Practices

When using this project, please follow these security best practices:

### 1. Keep Dependencies Updated
Regularly update your dependencies by running:
```shell
poetry update
```

### 2. Use Virtual Environments
Always use a Python virtual environment when working with this project:
```shell
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Review Code Changes
When updating to new versions, review the changelog and code changes for any security-related updates.

### 4. Secure Configuration
- Do not commit sensitive information (API keys, credentials, etc.) to version control
- Use environment variables for sensitive configuration
- Keep configuration files with sensitive data outside of the repository

### 5. Report Issues Responsibly
If you identify a security issue, please follow the responsible disclosure guidelines outlined above rather than creating a public issue or pull request.

## Security Considerations

This project is a benchmarking tool for LLM projects and does not directly handle sensitive data by default. However, users should be aware of the following:

- **Input Validation**: Ensure any external inputs are properly validated before use
- **Dependency Security**: Monitor dependencies for known vulnerabilities using tools like:
  - `poetry check`
  - GitHub's Dependabot
  - OWASP Dependency-Check

- **Python Version**: This project requires Python 3.8 or higher. Keep your Python installation up to date with the latest security patches

## License

This project is provided "as-is" and the security practices of the project are intended to minimize risks while the project operates in good faith with its users.

## Contact

For security concerns, please contact the project maintainers. Do not use the public issue tracker for security vulnerabilities.
