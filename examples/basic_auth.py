"""
Basic authentication example using iRacing OAuth client.

This demonstrates the simplest use case: authenticating and checking token status.
For more complex examples with data API access, see main.py and claim_steam.py.
"""

from iracing_oauth_client import IRacingOAuthClient, Config


def main():
    """Basic authentication example."""
    # Load configuration from .env file
    config = Config()

    # Create the OAuth client
    oauth_client = IRacingOAuthClient(
        client_id=config.client_id,
        client_secret=config.client_secret,
        username=config.username,
        password=config.password,
        request_timeout=config.request_timeout,
        token_refresh_buffer_seconds=config.token_refresh_buffer_seconds
    )

    # Authenticate
    if oauth_client.authenticate():
        print("Successfully authenticated!")
        print(f"Token expires at: {oauth_client.token_expires_at}")

        # Check if authenticated
        if oauth_client.is_authenticated():
            print("✅ Token is valid and ready to use")
    else:
        print("Authentication failed!")


if __name__ == "__main__":
    main()
