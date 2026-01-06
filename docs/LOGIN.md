# Microsoft-Style Login Page

> Implementation plan for a landing page that mirrors the Microsoft 365 login experience.

---

## 🎯 Objective

Replace the current custom login page with a Microsoft-branded login experience that:

1. Looks identical to the official Microsoft login at `login.microsoftonline.com`
2. Provides a seamless, familiar experience for Northstar employees
3. Redirects to Azure AD authentication on form submission
4. Maintains professional branding consistency

---

## 📸 Reference Design

The target design matches the official Microsoft login page:

### Visual Elements

| Element        | Description                                             |
| -------------- | ------------------------------------------------------- |
| **Background** | Light gradient (purple/blue/pink watercolor tones)      |
| **Card**       | White centered card with subtle shadow                  |
| **Logo**       | Microsoft 4-square logo with "Microsoft" text           |
| **Title**      | "Sign in" in bold, dark text                            |
| **Input**      | Email/phone/Skype placeholder, underline-style input    |
| **Links**      | Blue links: "Create one!", "Can't access your account?" |
| **Button**     | Blue "Next" button, full width within card              |
| **Footer**     | "Sign-in options" with key icon                         |

### Layout Specifications

```
┌─────────────────────────────────────────────────────────────────┐
│                    Gradient Background                          │
│                                                                 │
│              ┌─────────────────────────────┐                    │
│              │  ■ Microsoft                │                    │
│              │                             │                    │
│              │  Sign in                    │                    │
│              │                             │                    │
│              │  Email, phone, or Skype     │                    │
│              │  ─────────────────────────  │                    │
│              │                             │                    │
│              │  No account? Create one!    │                    │
│              │  Can't access your account? │                    │
│              │                             │                    │
│              │            ┌──────────┐     │                    │
│              │            │   Next   │     │                    │
│              │            └──────────┘     │                    │
│              └─────────────────────────────┘                    │
│                                                                 │
│              ┌─────────────────────────────┐                    │
│              │  🔑  Sign-in options        │                    │
│              └─────────────────────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Design Specifications

### Colors

```css
/* Microsoft Brand Colors */
--ms-blue: #0078d4;
--ms-blue-hover: #106ebe;
--ms-text-primary: #1b1b1b;
--ms-text-secondary: #605e5c;
--ms-link-blue: #0067b8;
--ms-border: #8a8886;
--ms-background-card: #ffffff;

/* Gradient Background */
--ms-gradient: linear-gradient(135deg, #f3e7e9 0%, #e3eeff 50%, #e8f4ea 100%);
```

### Typography

| Element           | Font     | Size | Weight | Color   |
| ----------------- | -------- | ---- | ------ | ------- |
| Logo text         | Segoe UI | 15px | 600    | #5e5e5e |
| Sign in           | Segoe UI | 24px | 600    | #1b1b1b |
| Input placeholder | Segoe UI | 15px | 400    | #605e5c |
| Links             | Segoe UI | 13px | 400    | #0067b8 |
| Button            | Segoe UI | 14px | 600    | #ffffff |
| Sign-in options   | Segoe UI | 13px | 400    | #1b1b1b |

### Card Dimensions

| Property      | Value                     |
| ------------- | ------------------------- |
| Width         | 440px (max)               |
| Padding       | 44px                      |
| Border radius | 0px (sharp corners)       |
| Box shadow    | 0 2px 6px rgba(0,0,0,0.2) |

### Input Field

| Property      | Value                     |
| ------------- | ------------------------- |
| Height        | 36px                      |
| Border        | none (bottom border only) |
| Border-bottom | 1px solid #8a8886         |
| Focus border  | 2px solid #0078d4         |
| Padding       | 6px 0                     |

### Button

| Property      | Value   |
| ------------- | ------- |
| Background    | #0078d4 |
| Hover         | #106ebe |
| Height        | 32px    |
| Min-width     | 108px   |
| Border radius | 0px     |
| Float         | right   |

---

## 📁 File Structure

```
templates/
├── login.html          # Microsoft-style login page
└── ...

static/
├── css/
│   ├── login.css       # Login-specific styles
│   └── ...
├── img/
│   ├── ms-logo.svg     # Microsoft 4-square logo
│   └── ...
└── ...
```

---

## 🔧 Implementation Steps

### Phase 1: HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sign in to your account</title>
    <link rel="stylesheet" href="/static/css/login.css" />
  </head>
  <body>
    <div class="login-background">
      <div class="login-container">
        <!-- Main Login Card -->
        <div class="login-card">
          <!-- Microsoft Logo -->
          <div class="logo-container">
            <img
              src="/static/img/ms-logo.svg"
              alt="Microsoft"
              class="ms-logo"
            />
            <span class="ms-logo-text">Microsoft</span>
          </div>

          <!-- Title -->
          <h1 class="sign-in-title">Sign in</h1>

          <!-- Login Form -->
          <form action="/auth/login" method="POST" id="login-form">
            <div class="input-container">
              <input
                type="text"
                id="email"
                name="email"
                placeholder="Email, phone, or Skype"
                autocomplete="username"
                required
              />
            </div>

            <!-- Links -->
            <div class="help-links">
              <p>No account? <a href="#">Create one!</a></p>
              <p><a href="#">Can't access your account?</a></p>
            </div>

            <!-- Submit Button -->
            <div class="button-container">
              <button type="submit" class="btn-next">Next</button>
            </div>
          </form>
        </div>

        <!-- Sign-in Options -->
        <div class="signin-options-card">
          <button class="btn-signin-options">
            <span class="key-icon">🔑</span>
            Sign-in options
          </button>
        </div>
      </div>
    </div>
  </body>
</html>
```

### Phase 2: CSS Styling

```css
/* login.css - Microsoft-style login */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
  min-height: 100vh;
}

.login-background {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    #f3e7e9 0%,
    #e3eeff 25%,
    #d4e4ed 50%,
    #e8f4ea 75%,
    #f3e7e9 100%
  );
}

.login-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.login-card {
  background: #ffffff;
  width: 440px;
  padding: 44px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 16px;
}

.ms-logo {
  width: 24px;
  height: 24px;
}

.ms-logo-text {
  font-size: 15px;
  font-weight: 600;
  color: #5e5e5e;
}

.sign-in-title {
  font-size: 24px;
  font-weight: 600;
  color: #1b1b1b;
  margin-bottom: 24px;
}

.input-container {
  margin-bottom: 24px;
}

.input-container input {
  width: 100%;
  height: 36px;
  border: none;
  border-bottom: 1px solid #8a8886;
  font-size: 15px;
  padding: 6px 0;
  outline: none;
}

.input-container input:focus {
  border-bottom: 2px solid #0078d4;
  margin-bottom: -1px;
}

.input-container input::placeholder {
  color: #605e5c;
}

.help-links {
  margin-bottom: 24px;
}

.help-links p {
  font-size: 13px;
  color: #1b1b1b;
  margin-bottom: 8px;
}

.help-links a {
  color: #0067b8;
  text-decoration: none;
}

.help-links a:hover {
  text-decoration: underline;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.btn-next {
  min-width: 108px;
  height: 32px;
  background: #0078d4;
  color: #ffffff;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0 20px;
}

.btn-next:hover {
  background: #106ebe;
}

.signin-options-card {
  background: #ffffff;
  width: 440px;
  padding: 16px 44px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.btn-signin-options {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  font-size: 13px;
  color: #1b1b1b;
  cursor: pointer;
  padding: 0;
}

.btn-signin-options:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .login-card,
  .signin-options-card {
    width: 100%;
    margin: 0 16px;
  }
}
```

### Phase 3: Form Behavior

```javascript
// login.js - Form handling

document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;

  // Validate email domain (optional - restrict to company domain)
  // if (!email.endsWith('@northstar-tech.com')) {
  //     showError('Please use your Northstar email address');
  //     return;
  // }

  // Redirect to Azure AD login
  // The email can be passed as login_hint for pre-filling
  window.location.href = `/auth/login?login_hint=${encodeURIComponent(email)}`;
});

// Handle Sign-in options click
document
  .querySelector(".btn-signin-options")
  .addEventListener("click", function () {
    // Show alternative sign-in methods (if any)
    alert("Alternative sign-in options coming soon");
  });
```

### Phase 4: Backend Route Update

```python
# app/routes/auth.py - Update login route

@auth_bp.route("/login")
def login():
    """Render Microsoft-style login page."""
    # If already logged in, redirect to app
    if "user" in session:
        return redirect(url_for("main.app"))

    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login_submit():
    """Handle login form submission - redirect to Azure AD."""
    email = request.form.get("email", "")

    # Build Azure AD authorization URL with login_hint
    auth_url = build_auth_url(login_hint=email)

    return redirect(auth_url)
```

---

## ✅ Acceptance Criteria

### Visual Accuracy

- [ ] Background matches Microsoft gradient (purple/blue/pink watercolor)
- [ ] Card is white with sharp corners and subtle shadow
- [ ] Microsoft logo appears correctly with "Microsoft" text
- [ ] "Sign in" title matches font size and weight
- [ ] Input field has underline-only border style
- [ ] Links are blue and positioned correctly
- [ ] "Next" button is blue, right-aligned
- [ ] "Sign-in options" footer card appears below

### Functionality

- [ ] Email input accepts text
- [ ] Form submits on Enter key or button click
- [ ] Submitting redirects to Azure AD with login_hint
- [ ] Responsive design works on mobile
- [ ] "Create one!" link is disabled or hidden
- [ ] "Can't access your account?" links to help

### Accessibility

- [ ] All form elements have proper labels
- [ ] Tab order is logical
- [ ] Focus states are visible
- [ ] Color contrast meets WCAG AA

---

## 🔗 Related Documentation

- [AZURE.md](AZURE.md) - Azure AD authentication setup
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Technical architecture
- [DARKMODE.md](DARKMODE.md) - Dark mode (may need login page variant)

---

## 📋 TODO

- [ ] Extract Microsoft logo SVG
- [ ] Create login.css stylesheet
- [ ] Update login.html template
- [ ] Test on multiple browsers
- [ ] Add loading state for "Next" button
- [ ] Consider dark mode variant
- [ ] Add error message display for failed logins

---

_Last updated: January 6, 2026_
