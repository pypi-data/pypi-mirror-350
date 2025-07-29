# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in Arc Tracing SDK, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via:

1. **Email**: Send details to security@arc-tracing.dev
2. **GitHub Security Advisory**: Use the [private vulnerability reporting feature](https://github.com/your-org/arc-tracing-sdk/security/advisories/new)

### What to Include

Please include the following information in your report:

- **Description**: A clear description of the vulnerability
- **Impact**: Potential impact and affected components
- **Reproduction**: Step-by-step instructions to reproduce the issue
- **Version**: The version(s) of Arc Tracing SDK affected
- **Environment**: Operating system, Python version, and other relevant details
- **Mitigation**: Any workarounds or mitigations you've identified

### Response Timeline

- **Initial Response**: Within 24 hours of receipt
- **Assessment**: Within 72 hours, we'll provide an assessment of the report
- **Resolution**: We aim to resolve critical vulnerabilities within 7 days
- **Disclosure**: Coordinated disclosure timeline will be discussed with the reporter

### Security Measures

Arc Tracing SDK implements several security measures:

#### Data Protection
- **Sensitive Data Filtering**: Automatic filtering of potentially sensitive information in traces
- **Configurable Redaction**: Ability to redact specific fields from trace data
- **Local Fallback**: Secure local storage when remote services are unavailable

#### Communication Security
- **TLS Encryption**: All communication with Arc platform uses TLS 1.2+
- **API Key Protection**: Secure handling and storage of API credentials
- **Request Validation**: Input validation and sanitization

#### Framework Integration Security
- **Non-Invasive Integration**: Integration adapters that don't modify framework internals
- **Isolation**: Tracing errors don't affect application functionality
- **Graceful Degradation**: Secure fallback when frameworks are unavailable

### Security Best Practices

When using Arc Tracing SDK:

#### Configuration
- Store API keys in environment variables, not in code
- Use configuration files with proper permissions (600)
- Regularly rotate API keys and credentials

#### Data Handling
- Review trace data for sensitive information before enabling in production
- Use custom redaction rules for sensitive fields
- Monitor trace exports for unexpected data

#### Updates
- Keep Arc Tracing SDK updated to the latest version
- Subscribe to security advisories and releases
- Test updates in non-production environments first

### Scope

This security policy applies to:

- Arc Tracing SDK core functionality
- Integration adapters for supported frameworks
- Configuration and credential handling
- Data export and transmission

### Out of Scope

This policy does not cover:

- Vulnerabilities in third-party frameworks (OpenAI, LangChain, etc.)
- Issues in the Arc platform itself
- Local development and testing environments
- Vulnerabilities requiring physical access to the system

### Security Updates

Security updates will be:

- Released as patch versions (e.g., 0.1.1 → 0.1.2)
- Documented in the changelog with security labels
- Announced through GitHub releases and security advisories
- Backported to supported versions when necessary

### Contact

For security-related questions or concerns:

- **Email**: security@arc-tracing.dev
- **GitHub**: Use private vulnerability reporting
- **General Questions**: Use GitHub Discussions for non-sensitive security questions

### Attribution

We appreciate responsible disclosure and will acknowledge security researchers who report vulnerabilities:

- Public acknowledgment in security advisories (with permission)
- Attribution in release notes and changelog
- Recognition in the project's security contributors list

Thank you for helping keep Arc Tracing SDK secure!