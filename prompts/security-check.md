# Security Check Prompt

## Security Validation Instructions

Please check through all the code you just wrote and make sure it follows security best practices. Make sure there are no sensitive information in the frontend and there are no vulnerabilities that can be exploited.

### Security Checklist

#### 1. **Sensitive Information Review**
- [ ] No API keys, passwords, or secrets in frontend code
- [ ] No database credentials exposed in client-side code
- [ ] No internal URLs or endpoints exposed unnecessarily
- [ ] No debug information that reveals system architecture
- [ ] Environment variables properly configured for sensitive data

#### 2. **Input Validation & Sanitization**
- [ ] All user inputs are validated and sanitized
- [ ] SQL injection prevention measures in place
- [ ] XSS (Cross-Site Scripting) protection implemented
- [ ] CSRF (Cross-Site Request Forgery) tokens where needed
- [ ] File upload restrictions and validation

#### 3. **Authentication & Authorization**
- [ ] Proper authentication mechanisms implemented
- [ ] Authorization checks on sensitive operations
- [ ] Session management secure (if applicable)
- [ ] Password security best practices followed
- [ ] Rate limiting on authentication endpoints
#### 4. **Data Protection**
- [ ] Sensitive data encrypted at rest and in transit
- [ ] HTTPS enforced for all communications
- [ ] Proper error handling without information leakage
- [ ] Logging doesn't expose sensitive information
- [ ] Data access follows principle of least privilege

#### 5. **Common Vulnerability Checks**
- [ ] No eval() or similar dangerous functions
- [ ] Dependencies are up-to-date and secure
- [ ] No hardcoded secrets or configurations
- [ ] Proper CORS configuration
- [ ] Security headers implemented where appropriate

### Security Report Format

After reviewing, provide a report in this format:

```markdown
## Security Review Report

### ✅ Security Measures Implemented
- [List of security practices found in the code]

### ⚠️ Potential Security Issues
- [Any vulnerabilities or concerns identified]

### 🔧 Recommended Improvements
- [Specific suggestions for enhancing security]

### 📋 Additional Security Considerations
- [Future security measures to consider]
```

### Critical Security Rules

- **Never expose secrets**: API keys, tokens, passwords must be server-side only
- **Validate everything**: All inputs must be validated and sanitized
- **Assume breach**: Code defensively assuming bad actors will try to exploit
- **Minimal exposure**: Only expose what's absolutely necessary
- **Regular updates**: Keep dependencies current and secure

**Remember**: Security is not optional. Better to be overly cautious than to leave vulnerabilities.