<p style="text-align:center;">
  <img src="https://i.ibb.co/b512JL9P/husktag.png" width="150px"/>
</p>
<h1 style="text-align:center;">HuskTag</h1>
<h2 style="text-align:center;">Tag It Quietly. Trace It Loudly.</h2>

## Table of Contents

1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Features](#features)
4. [Security Implementation](#security-implementation)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

## Project Overview

HuskTag is a secure tag management system with enterprise-grade protection features. The application provides user authentication, dashboard functionality, and administrative controls with a focus on security and responsive design.

## Folder Structure

```
HuskTag/
│
├── static/
│   ├── css/
│   │   └── style.css            # Custom styles overriding Bootstrap
│   ├── js/
│   │   └── main.js              # Main JavaScript functionality
│   └── images/
│       └── favicon.ico          # Application favicon
│
├── templates/
│   └── # Base template with security features
│
├── app/
│   ├── # Application factory
│   └── route/
│       └── # Main application routes
|
├── requirements.txt             # Python dependencies
├── config.py                    # Application configuration
├── README.md                    # This documentation file
└── main.py                      # Application entry point
```

## Features

### Core Functionality

- User authentication (login/registration)
- Responsive dashboard
- Administrative controls
- Secure tag management

### Security Features

- 256-bit encryption
- Two-factor authentication ready
- Secure HTTP headers (CSP, XSS protection)
- CSRF protection
- Security console warnings
- Encrypted connection indicators

### UI/UX Features

- Responsive Bootstrap 5 layout
- Font Awesome icons
- Google Fonts integration
- Flash message system with icons
- Persistent security status indicator
- Accessible navigation

## Security Implementation

### Frontend Security

```html
<meta
  http-equiv="Content-Security-Policy"
  content="default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"
/>
<meta http-equiv="X-Content-Type-Options" content="nosniff" />
<meta http-equiv="X-Frame-Options" content="DENY" />
<meta
  http-equiv="Strict-Transport-Security"
  content="max-age=63072000; includeSubDomains; preload"
/>
```

### Backend Security

- Flask-Talisman for HTTPS enforcement
- Flask-WTF CSRF protection
- Password hashing with Werkzeug
- Secure session management
- Admin privilege separation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/snehkr/husktag.git
   cd husktag
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the application:

   - Edit `config.py` with your settings
   - Set secret keys and database URI

5. Run the application:
   ```py
   python main.py
   ```

## Usage

### Accessing the Application

1. Open your browser to `http://localhost:5000`
2. Register a new account or login with existing credentials
3. Access the dashboard for tag management

### Admin Features

1. Login with an admin account
2. Access the admin panel via the navigation
3. View security logs and manage users

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Note**: This README assumes you have a basic Flask application structure. You may need to adjust file paths and configurations based on your specific implementation. The security features mentioned should be properly implemented in your Flask backend for full protection.
