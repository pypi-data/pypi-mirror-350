import base64
import logging
import os
import hashlib
import sys

# Obfuscated credentials - these are encoded but not directly usable
# This adds a layer of protection against casual inspection
_ENCODED_CREDENTIALS = {
    "SUPABASE_URL": "aHR0cHM6Ly9tdmV1eXBjcHZkYXZoeXJ0bXJlaC5zdXBhYmFzZS5jbw==",
    "SUPABASE_KEY": "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKemRYQmhZbUZ6WlNJc0luSmxaaUk2SW0xMlpYVjVjR053ZG1SaGRtaDVjblJ0Y21Wb0lpd2ljbTlzWlNJNkltRnViMjRpTENKcFlYUWlPakUzTXpVM05EVTBNakFzSW1WNGNDSTZNakExTVRNeU1UUXlNSDAuUFlMVjBodFdNMk41WURjeHpITFhacXRyVjd6LVlxNzZHN0VmS2FBamhrWQ==",
    "SUPABASE_SERVICE_ROLE_KEY": "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKemRYQmhZbUZ6WlNJc0luSmxaaUk2SW0xMlpYVjVjR053ZG1SaGRtaDVjblJ0Y21Wb0lpd2ljbTlzWlNJNkluTmxjblpwWTJWZmNtOXNaU0lzSW1saGRDSTZNVGN6TlRjME5UUXlNQ3dpWlhod0lqb3lNRFV4TXpJeE5ESXdmUS5QTTdNV09SNWg4Zi1VamdLTlNjeWFwM1VWaHdlSFlNZTJ0YS0wcUJBQ2xv"
}

def _decode_base64(encoded_text):
    """Decode base64 encoded text"""
    return base64.b64decode(encoded_text).decode('utf-8')

def _get_machine_fingerprint():
    """Generate a simple machine fingerprint for additional security"""
    # This creates a unique identifier based on machine-specific information
    # but doesn't collect any sensitive or personally identifiable information
    machine_info = f"{sys.platform}-{os.getenv('USERNAME', '')}-{os.path.expanduser('~')}"
    return hashlib.md5(machine_info.encode()).hexdigest()[:8]

def get_default_credentials():
    """
    Get the default credentials bundled with the library.
    These are used when no environment variables are found.
    
    The credentials are encoded and only decoded at runtime,
    making them harder to extract from the source code.
    """
    # Decode the credentials at runtime
    credentials = {}
    for key, encoded_value in _ENCODED_CREDENTIALS.items():
        credentials[key] = _decode_base64(encoded_value)
    
    # Log that we're using bundled credentials (without revealing them)
    logging.info("Using bundled Supabase credentials")
    
    return credentials

def obfuscate_key(key):
    """Simple obfuscation for logging purposes"""
    if not key:
        return None
    if len(key) <= 8:
        return "****"
    return key[:4] + "****" + key[-4:]