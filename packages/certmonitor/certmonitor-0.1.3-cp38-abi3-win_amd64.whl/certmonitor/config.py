# config.py

import os

# Default validators if not set in environment
DEFAULT_VALIDATORS = ["expiration", "hostname", "root_certificate"]

# Read from environment variable, fall back to default if not set
ENABLED_VALIDATORS = (
    os.environ.get("ENABLED_VALIDATORS", "").split(",") or DEFAULT_VALIDATORS
)

# Remove any empty strings that might result from splitting
ENABLED_VALIDATORS = [v.strip() for v in ENABLED_VALIDATORS if v.strip()]
