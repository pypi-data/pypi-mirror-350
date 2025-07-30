import importlib
import os
import ssl

from funcy import distinct, remove

from .helpers import (
    add_decode_responses_to_redis_url,
    array_from_string,
    cast_int_or_default,
    fix_assets_path,
    int_or_none,
    parse_boolean,
    set_from_string,
)

from .dynamic_settings import DynamicSettings

# Initialize dynamic settings
dynamic_settings = DynamicSettings()

SQLALCHEMY_MAX_OVERFLOW = int_or_none(os.environ.get("SQLALCHEMY_MAX_OVERFLOW"))
SQLALCHEMY_POOL_SIZE = int_or_none(os.environ.get("SQLALCHEMY_POOL_SIZE"))
SQLALCHEMY_DISABLE_POOL = parse_boolean(os.environ.get("SQLALCHEMY_DISABLE_POOL", "false"))
SQLALCHEMY_ENABLE_POOL_PRE_PING = parse_boolean(os.environ.get("SQLALCHEMY_ENABLE_POOL_PRE_PING", "false"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

AUTH_TYPE = os.environ.get("REDASH_AUTH_TYPE", "api_key")


# Whether and how to redirect non-HTTP requests to HTTPS. Disabled by default.
ENFORCE_HTTPS = parse_boolean(os.environ.get("REDASH_ENFORCE_HTTPS", "false"))
ENFORCE_HTTPS_PERMANENT = parse_boolean(os.environ.get("REDASH_ENFORCE_HTTPS_PERMANENT", "false"))
# Whether file downloads are enforced or not.
ENFORCE_FILE_SAVE = parse_boolean(os.environ.get("REDASH_ENFORCE_FILE_SAVE", "true"))

# Whether api calls using the json query runner will block private addresses
ENFORCE_PRIVATE_ADDRESS_BLOCK = parse_boolean(os.environ.get("REDASH_ENFORCE_PRIVATE_IP_BLOCK", "true"))

# Whether to use secure cookies by default.
COOKIES_SECURE = parse_boolean(os.environ.get("REDASH_COOKIES_SECURE", str(ENFORCE_HTTPS)))
# Whether the session cookie is set to secure.
SESSION_COOKIE_SECURE = parse_boolean(os.environ.get("REDASH_SESSION_COOKIE_SECURE") or str(COOKIES_SECURE))
# Whether the session cookie is set HttpOnly.
SESSION_COOKIE_HTTPONLY = parse_boolean(os.environ.get("REDASH_SESSION_COOKIE_HTTPONLY", "true"))
SESSION_EXPIRY_TIME = int(os.environ.get("REDASH_SESSION_EXPIRY_TIME", 60 * 60 * 6))

# Whether the session cookie is set to secure.
REMEMBER_COOKIE_SECURE = parse_boolean(os.environ.get("REDASH_REMEMBER_COOKIE_SECURE") or str(COOKIES_SECURE))
# Whether the remember cookie is set HttpOnly.
REMEMBER_COOKIE_HTTPONLY = parse_boolean(os.environ.get("REDASH_REMEMBER_COOKIE_HTTPONLY", "true"))
# The amount of time before the remember cookie expires.
REMEMBER_COOKIE_DURATION = int(os.environ.get("REDASH_REMEMBER_COOKIE_DURATION", 60 * 60 * 24 * 31))


# If Redash is behind a proxy it might sometimes receive a X-Forwarded-Proto of HTTP
# even if your actual Redash URL scheme is HTTPS. This will cause Flask to build
# the SAML redirect URL incorrect thus failing auth. This is especially common if
# you're behind a SSL/TCP configured AWS ELB or similar.
# This setting will force the URL scheme.
SAML_SCHEME_OVERRIDE = os.environ.get("REDASH_SAML_SCHEME_OVERRIDE", "")

SAML_ENCRYPTION_PEM_PATH = os.environ.get("REDASH_SAML_ENCRYPTION_PEM_PATH", "")
SAML_ENCRYPTION_CERT_PATH = os.environ.get("REDASH_SAML_ENCRYPTION_CERT_PATH", "")
SAML_ENCRYPTION_ENABLED = SAML_ENCRYPTION_PEM_PATH != "" and SAML_ENCRYPTION_CERT_PATH != ""


STATIC_ASSETS_PATH = fix_assets_path(os.environ.get("REDASH_STATIC_ASSETS_PATH", "../client/dist/"))
FLASK_TEMPLATE_PATH = fix_assets_path(os.environ.get("REDASH_FLASK_TEMPLATE_PATH", STATIC_ASSETS_PATH))
# Time limit (in seconds) for scheduled queries. Set this to -1 to execute without a time limit.
SCHEDULED_QUERY_TIME_LIMIT = int(os.environ.get("REDASH_SCHEDULED_QUERY_TIME_LIMIT", -1))

# Time limit (in seconds) for adhoc queries. Set this to -1 to execute without a time limit.
ADHOC_QUERY_TIME_LIMIT = int(os.environ.get("REDASH_ADHOC_QUERY_TIME_LIMIT", -1))

JOB_EXPIRY_TIME = int(os.environ.get("REDASH_JOB_EXPIRY_TIME", 3600 * 12))
JOB_DEFAULT_FAILURE_TTL = int(os.environ.get("REDASH_JOB_DEFAULT_FAILURE_TTL", 7 * 24 * 60 * 60))

LOG_LEVEL = os.environ.get("REDASH_LOG_LEVEL", "INFO")
LOG_STDOUT = parse_boolean(os.environ.get("REDASH_LOG_STDOUT", "false"))
LOG_PREFIX = os.environ.get("REDASH_LOG_PREFIX", "")
LOG_FORMAT = os.environ.get(
    "REDASH_LOG_FORMAT",
    LOG_PREFIX + "[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s",
)

# sqlparse
SQLPARSE_FORMAT_OPTIONS = {
    "reindent": parse_boolean(os.environ.get("SQLPARSE_FORMAT_REINDENT", "true")),
    "keyword_case": os.environ.get("SQLPARSE_FORMAT_KEYWORD_CASE", "upper"),
}

# requests
REQUESTS_ALLOW_REDIRECTS = parse_boolean(os.environ.get("REDASH_REQUESTS_ALLOW_REDIRECTS", "false"))

# Enforces CSRF token validation on API requests.
# This is turned off by default to avoid breaking any existing deployments but it is highly recommended to turn this toggle on to prevent CSRF attacks.
ENFORCE_CSRF = parse_boolean(os.environ.get("REDASH_ENFORCE_CSRF", "false"))

# Databricks
CSRF_TIME_LIMIT = int(os.environ.get("REDASH_CSRF_TIME_LIMIT", 3600 * 6))

# Enhance schema fetching
SCHEMA_RUN_TABLE_SIZE_CALCULATIONS = parse_boolean(
    os.environ.get("REDASH_SCHEMA_RUN_TABLE_SIZE_CALCULATIONS", "false")
)

# BigQuery
BIGQUERY_HTTP_TIMEOUT = int(os.environ.get("REDASH_BIGQUERY_HTTP_TIMEOUT", "600"))
