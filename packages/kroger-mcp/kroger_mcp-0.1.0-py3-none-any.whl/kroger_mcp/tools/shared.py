"""
Shared utilities and client management for Kroger MCP server
"""

import os
import socket
import threading
import time
import webbrowser
import json
from typing import Optional
from kroger_api.kroger_api import KrogerAPI
from kroger_api.auth import authenticate_user
from kroger_api.utils.env import load_and_validate_env, get_zip_code, get_redirect_uri
from kroger_api.utils.oauth import start_oauth_server, generate_random_state, extract_port_from_redirect_uri
from kroger_api.token_storage import load_token, save_token

# Global state for clients and preferred location
_authenticated_client: Optional[KrogerAPI] = None
_client_credentials_client: Optional[KrogerAPI] = None

# JSON files for configuration storage
PREFERENCES_FILE = "kroger_preferences.json"


def get_client_credentials_client() -> KrogerAPI:
    """Get or create a client credentials authenticated client for public data"""
    global _client_credentials_client
    
    if _client_credentials_client is None:
        try:
            load_and_validate_env(["KROGER_CLIENT_ID", "KROGER_CLIENT_SECRET"])
            _client_credentials_client = KrogerAPI()
            
            # Try to load existing token first
            token_file = ".kroger_token_client_product.compact.json"
            token_info = load_token(token_file)
            
            if token_info:
                # Test if the token is still valid
                _client_credentials_client.client.token_info = token_info
                if _client_credentials_client.test_current_token():
                    # Token is valid, use it
                    pass
                else:
                    # Token is invalid, get a new one
                    token_info = _client_credentials_client.authorization.get_token_with_client_credentials("product.compact")
            else:
                # No existing token, get a new one
                token_info = _client_credentials_client.authorization.get_token_with_client_credentials("product.compact")
        except Exception as e:
            raise Exception(f"Failed to get client credentials: {str(e)}")
    
    return _client_credentials_client


def get_authenticated_client() -> KrogerAPI:
    """Get or create a user-authenticated client for cart operations with browser-based OAuth"""
    global _authenticated_client
    
    if _authenticated_client is None:
        try:
            load_and_validate_env(["KROGER_CLIENT_ID", "KROGER_CLIENT_SECRET", "KROGER_REDIRECT_URI"])
            
            # Try to load existing user token first
            token_file = ".kroger_token_user.json"
            token_info = load_token(token_file)
            
            if token_info:
                # Test if the token is still valid
                _authenticated_client = KrogerAPI()
                _authenticated_client.client.token_info = token_info
                _authenticated_client.client.token_file = token_file
                
                if _authenticated_client.test_current_token():
                    # Token is valid, use it
                    return _authenticated_client
                else:
                    # Token is invalid, try to refresh it
                    if "refresh_token" in token_info:
                        try:
                            new_token_info = _authenticated_client.authorization.refresh_token(token_info["refresh_token"])
                            # Token refreshed successfully
                            return _authenticated_client
                        except Exception as e:
                            print(f"Token refresh failed: {str(e)}")
                            # Refresh failed, need to re-authenticate
                            _authenticated_client = None
            
            # No valid token available, need to authenticate with browser
            if _authenticated_client is None:
                _authenticated_client = _authenticate_with_browser()
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")
    
    return _authenticated_client


def _authenticate_with_browser() -> KrogerAPI:
    """Authenticate user by opening browser and handling OAuth flow"""
    server = None
    try:
        redirect_uri = get_redirect_uri()
        port = extract_port_from_redirect_uri(redirect_uri)
        
        # Check if port is already in use and try alternative ports
        original_port = port
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                # Test if port is available
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                # Port is available, break out of loop
                break
            except OSError:
                if attempt < max_attempts - 1:
                    port += 1
                    print(f"Port {port - 1} is in use, trying port {port}...")
                else:
                    raise Exception(f"Ports {original_port}-{port} are all in use. Please free up port {original_port} or restart your system.")
        
        # Update redirect URI if we had to change the port
        if port != original_port:
            redirect_uri = redirect_uri.replace(f":{original_port}", f":{port}")
            print(f"Using alternative port {port} for OAuth callback.")
        
        # Create the API client
        kroger = KrogerAPI()
        
        # Generate a random state value for security
        state = generate_random_state()
        
        # Variables to store the authorization code
        auth_code = None
        auth_state = None
        auth_event = threading.Event()
        auth_error = None
        
        # Callback for when the authorization code is received
        def on_code_received(code, received_state):
            nonlocal auth_code, auth_state, auth_error
            try:
                auth_code = code
                auth_state = received_state
                auth_event.set()
            except Exception as e:
                auth_error = str(e)
                auth_event.set()
        
        # Start the server to handle the OAuth2 redirect
        try:
            server, server_thread = start_oauth_server(port, on_code_received)
        except Exception as e:
            raise Exception(f"Failed to start OAuth server on port {port}: {str(e)}")
        
        try:
            # Get the authorization URL with the potentially updated redirect URI
            if port != original_port:
                # Temporarily override the redirect URI for this authentication
                original_redirect = os.environ.get('KROGER_REDIRECT_URI')
                os.environ['KROGER_REDIRECT_URI'] = redirect_uri
            
            auth_url = kroger.authorization.get_authorization_url(
                scope="cart.basic:write profile.compact",
                state=state
            )
            
            # Restore original redirect URI if we changed it
            if port != original_port and original_redirect:
                os.environ['KROGER_REDIRECT_URI'] = original_redirect
            
            print("\n" + "="*60)
            print("KROGER AUTHENTICATION REQUIRED")
            print("="*60)
            print("Opening your browser for Kroger login...")
            print("Please log in and authorize the application.")
            if port != original_port:
                print(f"Note: Using port {port} instead of {original_port} due to port conflict.")
            print("This window will close automatically after authentication.")
            print("If the browser doesn't open, copy this URL:")
            print(f"  {auth_url}")
            print("="*60)
            
            # Open the authorization URL in the default browser
            try:
                webbrowser.open(auth_url)
            except Exception as e:
                print(f"Could not open browser automatically: {e}")
                print("Please manually open the URL above in your browser.")
            
            # Wait for the authorization code (timeout after 5 minutes)
            if not auth_event.wait(timeout=300):
                raise Exception("Authentication timed out after 5 minutes. Please try again.")
            
            if auth_error:
                raise Exception(f"OAuth callback error: {auth_error}")
            
            if not auth_code:
                raise Exception("No authorization code received. Authentication may have been cancelled.")
            
            # Verify the state parameter to prevent CSRF attacks
            if auth_state != state:
                raise Exception(f"State mismatch. Expected {state}, got {auth_state}. This could be a security issue.")
            
            # Exchange the authorization code for an access token
            try:
                token_info = kroger.authorization.get_token_with_authorization_code(auth_code)
            except Exception as e:
                raise Exception(f"Failed to exchange authorization code for token: {str(e)}")
            
            print("\n" + "="*60)
            print("AUTHENTICATION SUCCESSFUL!")
            print("="*60)
            print("You can now use cart operations and user-specific features.")
            print("Your authentication token has been saved for future use.")
            print("="*60 + "\n")
            
            return kroger
        
        finally:
            # Ensure the server is shut down properly
            if server:
                try:
                    server.shutdown()
                    # Give it a moment to fully shut down
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Note: OAuth server cleanup had an issue: {e}")
    
    except Exception as e:
        error_msg = str(e)
        print(f"\nAuthentication failed: {error_msg}")
        print("\nTo resolve this issue:")
        print("1. Make sure KROGER_REDIRECT_URI is set correctly in your .env file")
        print("2. Ensure the redirect URI matches what's registered in Kroger Developer Portal")
        print("3. If port issues persist, restart Claude Desktop or try a different port")
        print("4. You can change the port by updating KROGER_REDIRECT_URI to http://localhost:8001/callback")
        print("5. Make sure you have a stable internet connection")
        
        # Re-raise with a cleaner error message
        if "timed out" in error_msg.lower():
            raise Exception("Authentication timed out. Please try again and complete the login process more quickly.")
        elif "port" in error_msg.lower():
            raise Exception(f"Port conflict: {error_msg}")
        elif "connection" in error_msg.lower():
            raise Exception(f"Connection error: {error_msg}")
        else:
            raise Exception(f"Authentication failed: {error_msg}")


def invalidate_authenticated_client():
    """Invalidate the authenticated client to force re-authentication"""
    global _authenticated_client
    _authenticated_client = None


def invalidate_client_credentials_client():
    """Invalidate the client credentials client to force re-authentication"""
    global _client_credentials_client
    _client_credentials_client = None


def _load_preferences() -> dict:
    """Load preferences from file"""
    try:
        if os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load preferences: {e}")
    return {"preferred_location_id": None}


def _save_preferences(preferences: dict) -> None:
    """Save preferences to file"""
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(preferences, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save preferences: {e}")


def get_preferred_location_id() -> Optional[str]:
    """Get the current preferred location ID from preferences file"""
    preferences = _load_preferences()
    return preferences.get("preferred_location_id")


def set_preferred_location_id(location_id: str) -> None:
    """Set the preferred location ID in preferences file"""
    preferences = _load_preferences()
    preferences["preferred_location_id"] = location_id
    _save_preferences(preferences)


def format_currency(value: Optional[float]) -> str:
    """Format a value as currency"""
    if value is None:
        return "N/A"
    return f"${value:.2f}"


def get_default_zip_code() -> str:
    """Get the default zip code from environment or fallback"""
    return get_zip_code(default="10001")
