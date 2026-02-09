# Angular Security Upgrade Guide

## ⚠️ CRITICAL: XSS Vulnerabilities in Angular 17.3.12

This guide explains how to upgrade Angular to fix critical XSS vulnerabilities.

---

## Current Status

**Current Version**: Angular 17.3.12
**Vulnerabilities**: Multiple XSS and XSRF token leakage issues
**Patched Versions**: Angular 19.2.18+, 20.3.16+, or 21.0.7+

---

## Option 1: Upgrade to Angular 19 (RECOMMENDED)

Angular 19.2.18+ is the minimum version with all security patches.

### Step 1: Backup Your Code
```bash
cd /home/runner/work/office/office
git add .
git commit -m "Backup before Angular upgrade"
```

### Step 2: Update Angular
```bash
cd frontend

# Update Angular CLI and Core to version 19
ng update @angular/cli@19 @angular/core@19 --force --allow-dirty

# Update other Angular packages
ng update @angular/animations@19 @angular/common@19 @angular/compiler@19 @angular/forms@19 @angular/platform-browser@19 @angular/platform-browser-dynamic@19 @angular/router@19

# Install dependencies
npm install --legacy-peer-deps
```

### Step 3: Test the Application
```bash
# Build the application
npm run build

# Run the application
npm start
```

### Step 4: Fix Breaking Changes (if any)

Angular 19 has some breaking changes from 17. Common issues:

1. **Router changes**: Check route configurations
2. **Form changes**: Verify reactive forms still work
3. **HttpClient**: Ensure HTTP interceptors work correctly
4. **Standalone components**: Should work without changes

Refer to: https://angular.dev/update-guide

---

## Option 2: Stay on Angular 17 with Mitigations (TEMPORARY)

If you cannot upgrade immediately, implement these security measures:

### 1. Add Content Security Policy

Create/update `frontend/src/index.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Officer Management System</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  
  <!-- SECURITY: Content Security Policy -->
  <meta http-equiv="Content-Security-Policy" 
        content="default-src 'self'; 
                 script-src 'self'; 
                 style-src 'self' 'unsafe-inline'; 
                 img-src 'self' data: https:; 
                 font-src 'self' data:; 
                 connect-src 'self' http://localhost:5000;">
</head>
<body>
  <app-root></app-root>
</body>
</html>
```

### 2. Sanitize All Dynamic Content

In all components that display user content:

```typescript
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

export class YourComponent {
  constructor(private sanitizer: DomSanitizer) {}
  
  sanitizeHtml(html: string): SafeHtml {
    return this.sanitizer.sanitize(SecurityContext.HTML, html) || '';
  }
}
```

### 3. Disable SVG/MathML Features

Remove or disable any features that allow:
- User-uploaded SVG files
- User-created SVG content
- MathML input
- Direct HTML rendering of user content

### 4. Use Absolute URLs Only

In all HTTP requests, use absolute URLs:

```typescript
// ✅ GOOD
http.get('http://localhost:5000/api/endpoint')

// ❌ BAD - Protocol-relative URL
http.get('//localhost:5000/api/endpoint')
```

### 5. Add Server-Side CSP Headers

In `backend/src/server.js`:

```javascript
// Add helmet for security headers
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'", "data:"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
}));
```

Install helmet:
```bash
cd backend
npm install helmet
```

---

## Option 3: Upgrade to Latest Angular (21.x)

For the most up-to-date security:

```bash
cd frontend
ng update @angular/cli@21 @angular/core@21 --force
npm install --legacy-peer-deps
```

**Note**: This is a major version jump (17 → 21) and may have significant breaking changes.

---

## Testing After Upgrade

### 1. Build Test
```bash
npm run build
```

### 2. Unit Tests (if present)
```bash
npm test
```

### 3. Manual Testing
- [ ] Login functionality works
- [ ] Dashboard loads and displays charts
- [ ] All CRUD operations work
- [ ] Navigation works correctly
- [ ] Forms submit properly
- [ ] No console errors

---

## Rollback Plan

If upgrade fails:

```bash
cd frontend
git checkout -- package.json package-lock.json
npm install --legacy-peer-deps
```

---

## Timeline Recommendation

**IMMEDIATE (Development)**:
- Implement CSP headers
- Sanitize all dynamic content
- Disable SVG/MathML features

**WITHIN 1 WEEK (Before Production)**:
- Upgrade to Angular 19.2.18+
- Test all functionality
- Fix any breaking changes

**BEFORE PRODUCTION DEPLOYMENT**:
- ✅ Angular 19.2.18+ installed
- ✅ All tests passing
- ✅ CSP headers active
- ✅ Rate limiting implemented
- ✅ Security audit completed

---

## Support Resources

- Angular Update Guide: https://angular.dev/update-guide
- Angular Security: https://angular.dev/best-practices/security
- CSP Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- Angular Advisory: https://github.com/angular/angular/security/advisories

---

**Priority**: CRITICAL
**Required Before Production**: YES
**Estimated Time**: 2-4 hours for upgrade + testing
