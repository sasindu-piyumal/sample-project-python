# Security Policy for llm-benchmarking-py

## Table of Contents

- [Reporting Security Vulnerabilities](#reporting-security-vulnerabilities)
- [Responsible Disclosure](#responsible-disclosure)
- [Security Update Process](#security-update-process)
- [Security Best Practices](#security-best-practices)
- [Security Scanning & Tools](#security-scanning--tools)
- [Known Limitations & Scope](#known-limitations--scope)
- [Frequently Asked Questions](#frequently-asked-questions)

---

## Reporting Security Vulnerabilities

### How to Report

We take security vulnerabilities seriously and appreciate responsible disclosure. If you discover a security vulnerability in llm-benchmarking-py, please report it **privately** by emailing:

**Email:** matthew.truscott@turintech.ai

**Subject Line:** `[SECURITY] Vulnerability Report - llm-benchmarking-py`

### What to Include

Please provide the following information to help us understand and address the vulnerability:

1. **Description**: A clear explanation of the vulnerability
2. **Location**: The specific file(s), module(s), and line numbers affected
3. **Reproduction Steps**: Step-by-step instructions to reproduce the issue
4. **Proof of Concept**: If possible, include a minimal reproducible example
5. **Impact**: The potential security impact and risk level
6. **Suggested Fix** (optional): Any proposed remediation if you have one

### What NOT to Include

- **Do not** publicly disclose the vulnerability before we've had a chance to address it
- **Do not** exploit the vulnerability beyond testing its existence
- **Do not** modify data, execute code, or access systems without permission
- **Do not** include any sensitive data or system credentials

---

## Responsible Disclosure

### Timeline

We commit to the following responsible disclosure timeline:

| Phase | Timeframe | Details |
|-------|-----------|---------|
| **Initial Response** | Within 48 hours | Acknowledgment of report receipt and initial assessment |
| **Investigation** | 1-2 weeks | Security team investigates and assesses severity |
| **Fix Development** | 2-4 weeks | Development and testing of security patch (varies by severity) |
| **Fix Deployment** | Upon completion | Release of patched version with security advisory |
| **Public Disclosure** | Coordinated timing | Announcement 30 days after patch release (minimum) |

### Severity Levels

We classify vulnerabilities using the following severity scale:

- **CRITICAL**: Immediate risk to users; potential for widespread harm; requires immediate patching
- **HIGH**: Significant security risk; potential unauthorized access or data exposure; patch within 2 weeks
- **MEDIUM**: Moderate security impact; requires defensive coding; patch within 4 weeks
- **LOW**: Limited security impact; good practice improvements; included in next regular release

### Acknowledgment

We recognize and publicly credit security researchers (with permission) who report vulnerabilities responsibly. If you'd like to be acknowledged, please let us know in your report.

---

## Security Update Process

### Notification Methods

Users will be notified of security updates through:

1. **GitHub Releases**: Security advisories published on the project's releases page
2. **Email Notification** (for critical vulnerabilities): If you've starred or watched the repository
3. **Security Advisories**: GitHub Security Advisory database
4. **Project Documentation**: Updates to this SECURITY.md file

### Patch Releases

- Security fixes are released as soon as possible after verification
- Patches are released with clear version bumps following semantic versioning
- Release notes include a security advisory explaining the fix
- Previous versions may receive backported security patches if actively maintained

### End of Life

Users are encouraged to keep llm-benchmarking-py updated to the latest version to receive security patches. As this project evolves:

- **Current Release (0.1.x)**: Receives all security patches
- **Previous Releases**: May receive critical security patches depending on impact
- **Deprecated Versions**: Security support ends 12 months after a new major version

---

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   - Run `poetry update` regularly to receive security patches
   - Review dependency changelogs for security notices
   - Use `poetry install --no-dev` in production environments

2. **Input Validation**
   - Never pass untrusted input to SQL queries
   - The project uses parameterized queries (?) for SQL safety
   - Validate and sanitize all external inputs before processing
   - See detailed best practices in [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md) (when available)

3. **Data Protection**
   - SQLite databases should be stored securely with proper file permissions
   - Avoid storing sensitive data in benchmarking datasets
   - Disable database file public access in production environments

4. **Environment Configuration**
   - Store credentials and secrets outside the codebase
   - Use environment variables for configuration
   - Never commit `.env` files or secrets to version control

5. **Logging Security**
   - Be cautious about logging sensitive information
   - Review logs regularly for suspicious activity
   - Implement log rotation and retention policies

### For Contributors

1. **Code Security**
   - Follow OWASP secure coding principles
   - Use type hints (mypy enabled) to catch type-related bugs early
   - Write unit tests for security-critical code paths
   - Review existing security tests when adding new features

2. **Dependency Management**
   - Minimize external dependencies to reduce attack surface
   - Regularly audit dependencies for known vulnerabilities
   - Update dependencies proactively
   - Document the security rationale for each dependency

3. **Code Review**
   - All code changes require review before merging
   - Pay special attention to security implications in PR reviews
   - Review changes to database query code carefully
   - Verify input handling and validation logic

4. **Testing**
   - Write tests for both functionality and security edge cases
   - Test with invalid, malformed, and malicious inputs
   - Include regression tests when fixing security issues
   - Use pytest to ensure comprehensive test coverage

---

## Security Scanning & Tools

### Integrated Security Tools

The project uses the following security tools to identify and prevent vulnerabilities:

#### Static Analysis

- **[mypy](https://www.mypy-lang.org/)**: Python type checker for identifying type-related bugs that could lead to runtime errors
  - Enabled for all modules
  - Configuration: See `pyproject.toml`
  - Usage: Type hints help prevent logic errors and security issues

#### Planned Security Tools

The following tools are planned for integration:

- **[bandit](https://bandit.readthedocs.io/)**: Security linter for identifying common security issues
  - Will scan for SQL injection, hardcoded passwords, use of insecure functions
  - Run: `poetry run bandit -r src/`

- **[safety](https://safety.readthedocs.io/)**: Checks dependencies for known security vulnerabilities
  - Will audit Poetry lock file against known vulnerability database
  - Run: `poetry run safety check`

- **[pylint](https://www.pylint.org/)**: Code quality and security static analysis
  - Will detect potential security issues and code smells
  - Run: `poetry run pylint src/`

### Running Security Checks

Once security tools are configured, run comprehensive checks with:

```bash
# Check Python type safety
poetry run mypy src/

# Scan for security issues (when bandit is added)
poetry run bandit -r src/

# Audit dependencies (when safety is added)
poetry run safety check

# Run all tests including security regression tests
poetry run pytest --benchmark-skip tests/
```

### Continuous Integration

Security scanning can be integrated into CI/CD pipelines. Recommended checks:

1. Run type checking on all pull requests
2. Scan for known vulnerable dependencies
3. Execute the full test suite including security tests
4. Verify code follows established security best practices

---

## Known Limitations & Scope

### Security Scope

This project is a **benchmarking and algorithm library** with the following scope and limitations:

#### In Scope

- Secure handling of input data passed to algorithms
- Parameterized SQL queries to prevent SQL injection
- Type safety through mypy type checking
- Secure random data generation for benchmarking
- Safe file operations for log and database handling

#### Out of Scope

- **Network Security**: This project does not implement network communication. Users are responsible for securing any network transport of data.
- **Encryption**: The project does not implement cryptographic functions. For secure data storage, use Python's `cryptography` library or system-level encryption.
- **Authentication & Authorization**: Not implemented in this library. Deploy with appropriate authentication mechanisms in your application.
- **Production Data Handling**: This is a benchmarking tool, not a production data processing system. Do not process sensitive personal data without appropriate safeguards.

### Known Limitations

1. **SQLite Database Security**
   - SQLite is suitable for development and testing but has limitations for high-security environments
   - SQLite does not support user-level access control
   - For production systems handling sensitive data, consider PostgreSQL or MySQL with proper security configuration

2. **File Permissions**
   - The project creates logs in a `logs/` directory and accesses SQLite databases
   - Users are responsible for ensuring appropriate file system permissions
   - In multi-user systems, configure umask appropriately (typically 0077 for logs containing sensitive info)

3. **Python Version**
   - Supported versions: Python 3.8+
   - Older Python versions may have unpatched security vulnerabilities
   - Always use the latest stable Python release for your major version

4. **Benchmarking Data**
   - Benchmarking datasets may include generated data that should not be used for production
   - Random data generation uses Python's `random` module, not cryptographically secure random functions
   - For cryptographic use cases, use `secrets` or `os.urandom()`

5. **Open Source Nature**
   - This is an open-source project under active development (version 0.1.0)
   - Security is continuously improved, but no code is 100% secure
   - Use at your own risk and implement defense-in-depth strategies

### Compatibility & Support

- **Python 3.8+**: Security updates for Python should be applied independently
- **Poetry Package Manager**: Keep Poetry updated to receive security patches
- **Development Dependencies**: Keep black, isort, and pytest updated

---

## Frequently Asked Questions

### Q: How long until I get a response to my vulnerability report?

**A:** We aim to acknowledge all vulnerability reports within 48 hours. The investigation timeline depends on severity (see [Timeline](#timeline) section).

### Q: Should I use this project in production?

**A:** This is a benchmarking library (v0.1.0). It can be used in production with understanding of its limitations. Implement appropriate security controls around data handling, authentication, and access control at the application level.

### Q: What if I find a vulnerability in a dependency?

**A:** If you discover a vulnerability in a dependency (e.g., pytest, Poetry), please:
1. Report it to the upstream project
2. Notify us so we can audit our dependency tree
3. Update to patched versions as soon as available

### Q: Are security advisories published for all issues?

**A:** Security advisories are published for:
- **CRITICAL & HIGH severity** vulnerabilities: Immediate public disclosure after patches are available
- **MEDIUM severity**: Disclosed after 30 days or next release
- **LOW severity**: May be fixed in regular updates without a security advisory

### Q: Can I discuss a vulnerability I found on GitHub Issues?

**A:** **No.** Please use the private email reporting mechanism (see [How to Report](#how-to-report)). Do not create public GitHub issues for security vulnerabilities.

### Q: Will my name be public if I report a vulnerability?

**A:** No, unless you explicitly request credit. We will respect your preference for privacy or attribution.

---

## Additional Resources

- **README.md**: Project overview and quick start guide
- **pyproject.toml**: Dependency list and project configuration
- **DOCUMENTATION_INDEX.md**: Guide to all project documentation
- **Tests**: Security regression tests located in `tests/` directory

For additional security documentation being developed:
- **SECURITY_BEST_PRACTICES.md**: Detailed input validation and error handling guidelines
- **SECURITY_CHECKLIST.md**: Security verification checklist for development

---

## Version History

- **v1.0** (Current): Initial public security policy
- **Policy Last Updated**: [Date will be updated with each revision]
- **Next Review**: Quarterly security review scheduled

---

## Contact & Support

For security-related inquiries:

- **Email**: matthew.truscott@turintech.ai
- **GitHub**: Open issues for non-security topics
- **Documentation**: See this file for comprehensive security guidance

---

**Thank you for helping us keep llm-benchmarking-py secure!** We appreciate the security research community's efforts to identify and responsibly disclose vulnerabilities.

