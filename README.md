# Login with Webex Flask

A sample Flask application that implements Login With Webex, OpenID Connect, Authorization Code Flow. This Python web application demonstrates how to integrate Webex authentication into a Flask-based web application using the standard OAuth 2.0 Authorization Code flow.

## 🎯 Overview

This Flask application provides a complete implementation of the Webex OpenID Connect authentication flow, including:

- **OAuth 2.0 Authorization Code Flow**: Secure server-side authentication
- **JWT Token Parsing**: Decoding and validating ID tokens
- **User Information Retrieval**: Accessing user profile data via the UserInfo endpoint
- **Session Management**: Secure storage of tokens and user state
- **Responsive Web Interface**: Clean, modern UI with Webex branding

## 🔧 Dependencies

This project relies on several Python packages:

- **Flask**: Web framework for Python
- **Requests**: HTTP library for API calls
- **JSON**: JSON parsing and manipulation (built-in)
- **JWT**: JSON Web Token handling
- **OS**: Operating system interface (built-in)
- **webbrowser**: Web browser launching (built-in)

## 🚀 Installation

Before you can run the project, you'll need to install the necessary dependencies. Here's how to do it:

### Prerequisites

1. **Python 3**: Make sure you have Python 3 installed on your machine. You can check this by running `python3 --version` in your command line. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).

2. **pip3**: Install the necessary packages using pip3. pip3 is a package manager for Python. You can install it following [these instructions](https://pip.pypa.io/en/stable/installing/).

### Install Dependencies

Once you have pip3 installed, you can install the packages with the following commands:

```bash
pip3 install Flask
pip3 install requests
pip3 install jwt
```

**Note**: The json and os packages are part of the Python Standard Library, so you don't need to install them separately.

### Alternative: Using requirements.txt

For easier dependency management, you can create a `requirements.txt` file:

```txt
Flask==2.3.3
requests==2.31.0
PyJWT==2.8.0
```

Then install with:
```bash
pip3 install -r requirements.txt
```

## ⚙️ Configuration

### 1. Webex Integration Setup

Before running the application, you need to configure your Webex Integration:

1. **Go to Webex Developer Portal**: https://developer.webex.com/
2. **Create a New Integration**: Click "Create an Integration"
3. **Configure Integration Settings**:
   - **Name**: Your application name
   - **Description**: Brief description of your app
   - **Redirect URI**: `http://0.0.0.0:10060/oauth`
   - **Scopes**: `openid`, `email`, `profile` (minimum required)

### 2. Application Configuration

Update the configuration variables in `login.py`:

```python
clientID = "YOUR CLIENT ID HERE"  # Replace with your Integration Client ID
secretID = "YOUR CLIENT SECRET HERE"  # Replace with your Integration Client Secret
redirectURI = "http://0.0.0.0:10060/oauth"  # Update if using different host/port
```

### 3. OAuth URL Configuration

Update the OAuth URL in `templates/index.html`:

```html
<a href='https://webexapis.com/v1/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://0.0.0.0:10060/oauth&scope=openid%20email%20profile&state=1234abcd'>
```

Replace `YOUR_CLIENT_ID` with your actual Client ID.

## 🏃 Usage

After installing the dependencies and configuring the application, you can run the script using Python in your command line:

```bash
python3 login.py
```

The application will start and be available at:
- **Local Access**: http://127.0.0.1:10060
- **Network Access**: http://0.0.0.0:10060

## 📁 Project Structure

```
login-with-webex-flask/
├── login.py              # Main Flask application
├── templates/            # HTML templates
│   ├── temp.html        # Base template
│   ├── index.html       # Login page
│   └── user.html        # User profile page
├── static/              # Static assets
│   └── css/
│       ├── index.css    # Stylesheet
│       └── logo.png     # Webex logo
├── LICENSE              # MIT License
└── README.md           # This file
```

## 🔍 Application Flow

### Step 1: Initial Authorization Request

1. User visits the main page (`/`)
2. User clicks the "GRANT" button
3. Application redirects to Webex authorization endpoint
4. User logs in with Webex credentials
5. User grants permission to the application

### Step 2: Authorization Code Exchange

1. Webex redirects back to `/oauth` with authorization code
2. Application validates the state parameter
3. Application exchanges authorization code for tokens
4. ID token and access token are stored in session

### Step 3: User Information Display

1. Application parses the ID token to extract claims
2. Application calls UserInfo endpoint with access token
3. User profile information is displayed

## 🔐 Security Features

### State Parameter Validation

The application uses a hardcoded state parameter (`1234abcd`) for CSRF protection:

```python
if state == '1234abcd':
    # Process authorization code
else:
    # Redirect back to login
```

### Session Management

Tokens are securely stored in Flask sessions:

```python
session['id_token'] = id_token 
session['access_token'] = access_token
```

### JWT Token Parsing

ID tokens are parsed without signature verification for demonstration:

```python
def parse_jwt(token):
    return jwt.decode(token, options={"verify_signature": False})
```

⚠️ **Production Note**: In production, you should validate JWT signatures.

## 📊 API Endpoints

### Flask Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main login page |
| `/oauth` | GET | OAuth callback handler |

### Webex API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `https://webexapis.com/v1/authorize` | Authorization endpoint |
| `https://webexapis.com/v1/access_token` | Token exchange endpoint |
| `https://webexapis.com/v1/userinfo` | User information endpoint |

## 🔧 Key Functions

### `get_tokens(code)`

Exchanges authorization code for access and ID tokens:

```python
def get_tokens(code):
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
               "code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    
    id_token = results["id_token"]
    access_token = results["access_token"]
    session['id_token'] = id_token 
    session['access_token'] = access_token
```

### `user_info()`

Retrieves user profile information:

```python
def user_info():
    accessToken = session['access_token']
    url = "https://webexapis.com/v1/userinfo"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + accessToken}
    req = requests.get(url=url, headers=headers)
    results = json.loads(req.text)
    return results
```

### `parse_jwt(token)`

Parses JWT tokens to extract claims:

```python
def parse_jwt(token):
    return jwt.decode(token, options={"verify_signature": False})
```

## 🎨 User Interface

### Design Elements

- **Clean, centered layout** with Webex branding
- **Responsive design** that works on various screen sizes
- **Webex color scheme** (blue: #0c99d5)
- **Professional typography** using Tahoma font

### Page Components

**Login Page (`index.html`)**:
- Webex logo
- "GRANT INTEGRATION ACCESS" heading
- Large "GRANT" button that initiates OAuth flow

**User Profile Page (`user.html`)**:
- User claims from ID token
- Complete user information from UserInfo endpoint

## 🧪 Testing

### Local Testing

1. **Start the application**:
   ```bash
   python3 login.py
   ```

2. **Open in browser**:
   Navigate to `http://127.0.0.1:10060`

3. **Test OAuth flow**:
   - Click "GRANT" button
   - Log in with Webex credentials
   - Verify user information is displayed

### Debug Mode

Enable debug mode for development:

```python
app.run("0.0.0.0", port=10060, debug=True)
```

This provides:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

## 🔍 Troubleshooting

### Common Issues

**Import Errors**
```bash
ModuleNotFoundError: No module named 'flask'
```
*Solution*: Install missing dependencies with `pip3 install flask`

**Configuration Errors**
```
Invalid client_id parameter
```
*Solution*: Verify Client ID and Secret are correctly configured

**Redirect URI Mismatch**
```
redirect_uri_mismatch
```
*Solution*: Ensure redirect URI in code matches Integration settings

**Token Exchange Failures**
```
invalid_grant
```
*Solution*: Check authorization code hasn't expired (10 minutes max)

### Debug Information

The application prints debug information to the console:

```python
print("function : get_tokens()")
print("code:", code)
print("ID Token stored in session : ", session['id_token'])
print("Access Token stored in session : ", session['access_token'])
print('claims : ', claims)
```

## 🔒 Security Considerations

### Production Deployment

For production use, consider:

1. **Environment Variables**: Store secrets in environment variables
   ```python
   clientID = os.getenv('WEBEX_CLIENT_ID')
   secretID = os.getenv('WEBEX_CLIENT_SECRET')
   ```

2. **HTTPS**: Use HTTPS in production
   ```python
   # Remove this line in production
   os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
   ```

3. **Secret Key**: Use a proper secret key
   ```python
   app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
   ```

4. **JWT Validation**: Implement proper JWT signature validation
   ```python
   def parse_jwt(token):
       # In production, validate signature
       return jwt.decode(token, key=jwk_key, algorithms=['RS256'])
   ```

### Data Protection

- **Session Security**: Uses secure session management
- **Token Storage**: Tokens stored in server-side sessions
- **State Validation**: CSRF protection via state parameter

## 📈 Advanced Features

### Custom Scopes

Add additional scopes for extended functionality:

```python
# In OAuth URL
scope = "openid email profile spark:people_read spark:rooms_read"
```

### Token Refresh

Implement token refresh for long-running sessions:

```python
def refresh_token():
    refresh_token = session.get('refresh_token')
    # Implement refresh logic
```

### User Profile Caching

Cache user information to reduce API calls:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_user_info(access_token):
    # Cached user info retrieval
```

## 🌐 Deployment

### Local Development

```bash
python3 login.py
```

### Production Deployment

**Using Gunicorn**:
```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:10060 login:app
```

**Using Docker**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 10060

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10060", "login:app"]
```

### Environment Configuration

Create a `.env` file:
```
WEBEX_CLIENT_ID=your_client_id_here
WEBEX_CLIENT_SECRET=your_client_secret_here
FLASK_SECRET_KEY=your_secret_key_here
REDIRECT_URI=https://yourdomain.com/oauth
```

## 🤝 Contributing

Please make sure to update tests as appropriate.

### Development Guidelines

1. **Code Style**: Follow PEP 8 Python style guidelines
2. **Documentation**: Add docstrings for new functions
3. **Testing**: Test OAuth flow with different user accounts
4. **Security**: Follow security best practices for token handling

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with detailed description

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

## 📚 Additional Resources

- [Webex Developer Portal](https://developer.webex.com/)
- [Login with Webex Documentation](https://developer.webex.com/docs/login-with-webex)
- [OAuth 2.0 Authorization Code Flow](https://tools.ietf.org/html/rfc6749#section-4.1)
- [OpenID Connect Specification](https://openid.net/connect/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🔗 Related Projects

- [Login with Webex (JavaScript)](https://github.com/WebexSamples/login-with-webex)
- [Webex OAuth Integration Sample](https://github.com/WebexSamples/webex-oauth-integration)
- [Webex Bot Framework](https://github.com/WebexCommunity/webex-node-bot-framework)

## 🆘 Support

- Create an issue in this repository
- Review [Webex Developer Documentation](https://developer.webex.com/docs)
- Contact [Webex Developer Support](https://developer.webex.com/support)

---

```
                _               
  __      _____| |__   _____  __
  \ \ /\ / / _ \ '_ \ / _ \ \/ /
   \ V  V /  __/ |_) |  __/>  <         @WebexDevs
    \_/\_/ \___|_.__/ \___/_/\_\
```

**Repository**: https://github.com/WebexSamples/login-with-webex-flask
