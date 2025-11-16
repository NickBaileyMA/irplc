# iRacing Password Limited OAuth Client

An example Python client library for authenticating with iRacing's OAuth provider using the
[Password Limited Flow](https://oauth.iracing.com/oauth2/book/password_limited_flow.html).

There are no plans to expand this repo to include Authorization Code Flow.

***This is not an official iRacing library and is not officially supported by iRacing.***

## Installation

### From Source

```bash
git clone https://github.com/NickBaileyMA/ir-pw-limited-client.git
cd ir-pw-limited-client
pip install -e .
```

### For Development

```bash
pip install -e ".[dev]"
```

## Architecture

The main part of the package provides:

- **IRacingOAuthClient**: Handles OAuth authentication, token management, and refresh
- **Config**: Manages configuration from environment variables
- **logging_utils**: Shared logging utilities (JSONFormatter, logger creation)

The examples directory shows how to integrate the OAuth client:
- **IRacingDataAPI**: Example implementation of a data retrieval wrapper
- **main.py**: Complete application example with looping API calls

### Logging Configuration

The application supports configurable logging with the following options:

**Log Levels:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- `DEBUG`: Verbose output for development (***sensitive info will be logged***)
- `INFO`: General information (default)
- `WARNING`: Warning messages only
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

## Usage

### Basic Usage

```python
from iracing_oauth_client import IRacingOAuthClient, Config

# Load configuration from .env file
config = Config()

# Create OAuth client
client = IRacingOAuthClient(
    client_id=config.client_id,
    client_secret=config.client_secret,
    username=config.username,
    password=config.password,
    request_timeout=config.request_timeout,
    token_refresh_buffer_seconds=config.token_refresh_buffer_seconds
)

# Authenticate
if client.authenticate():
    print("Successfully authenticated!")
    print(f"Token expires at: {client.token_expires_at}")
else:
    print("Authentication failed!")
```

### Run the Example Application

This will authenticate and demonstrate various API calls.

```bash
# Single iteration (for testing)
cd examples
python main.py

# Loop mode (requests every 3 minutes for 24 minutes)
# This is intended to demonstrate token refresh.
cd examples
python main.py --loop
```

## Configuration Options

Available environment variables in `.env`:

```ini
# Required
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USERNAME=your_username@example.com
PASSWORD=your_password

# Optional
SCOPE=iracing.auth
REQUEST_TIMEOUT=30
TOKEN_REFRESH_BUFFER_SECONDS=60
LOG_LEVEL=INFO
LOG_FORMAT=human
```

## Important Notes

- Only works for pre-registered clients and users
- The client automatically refreshes tokens when needed
- Password Limited Grant has strict rate limits on authentication
    - Use refresh tokens instead of re-authenticating all the time
    - Store tokens securely for reuse across sessions

## Development Note

This project was primarily developed using AI (Claude Sonnet) as a test of the iRacing OAuth documentation available at
https://oauth.iracing.com/oauth2/book/. The goal was to evaluate how well the documentation supports implementation by
following the Password Limited Grant flow specifications and examples provided. The initial prompt was:

> I want to create, in Python, a skeleton app that uses iRacing's OAuth solution to retrieve data from the iRacing /data
> API. I would be using the Password Limited Flow described at
> https://oauth.iracing.com/oauth2/book/password_limited_flow.html and further at
> https://oauth.iracing.com/oauth2/book/token_endpoint.html#password-limited-grant.

The AI did create a working OAuth client on the first prompt, but some additional changes were desired around logging &
error handling was mostly missing. It also didn't handle the `/data` API's JSON for JSON style results. The final
product, version `0.1.0` is a culmination of several prompts, human review and manual changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.