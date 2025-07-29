"""
Logging utilities for the SQLite adapter.

This module provides logging functionality with built-in sanitization
of sensitive data in queries and results.
"""

import logging
import re
from typing import Any, Dict, List, Optional, Union
from .type_defs import Parameters, Result, Row

# Configure logger
logger = logging.getLogger(__name__)

# Patterns for sensitive data
SENSITIVE_PATTERNS = [
    r'(password\s*=\s*[\'"][^\'"]+[\'"])',
    r'(passwd\s*=\s*[\'"][^\'"]+[\'"])',
    r'(secret\s*=\s*[\'"][^\'"]+[\'"])',
    r'(key\s*=\s*[\'"][^\'"]+[\'"])',
    r'(token\s*=\s*[\'"][^\'"]+[\'"])',
    r'(auth\s*=\s*[\'"][^\'"]+[\'"])',
    r'(credential\s*=\s*[\'"][^\'"]+[\'"])',
]

# Sensitive column names
SENSITIVE_COLUMNS = {
    'password', 'passwd', 'secret', 'key', 'token',
    'auth', 'credential', 'api_key', 'private_key',
    'access_token', 'refresh_token', 'ssn', 'credit_card',
    'card_number', 'cvv', 'pin', 'security_code',
    'name', 'email', 'phone', 'address', 'username'  # Added common PII fields
}


def sanitize_query(query: str) -> str:
    """Sanitize a query for logging.

    Args:
        query: SQL query to sanitize

    Returns:
        Sanitized query string
    """
    return " ".join(query.split())


def sanitize_parameters(parameters: Parameters) -> Parameters:
    """Sanitize parameters for logging.

    Args:
        parameters: Query parameters to sanitize.

    Returns:
        Sanitized parameters with sensitive values masked.
    """
    if parameters is None:
        return None

    if isinstance(parameters, (list, tuple)):
        return type(parameters)("***" for _ in parameters)
    elif isinstance(parameters, dict):
        return {k: "***" for k in parameters}
    else:
        return parameters


def sanitize_row(row: Row) -> Row:
    """Sanitize a row for logging.

    Args:
        row: Row to sanitize

    Returns:
        Sanitized row with sensitive values masked but IDs preserved.
    """
    sanitized_row = {}
    for k, v in row.items():
        # Keep numeric IDs and other non-sensitive fields intact
        if k.lower() == 'id' or k.endswith('_id') or k == 'rowcount' or k == 'lastrowid':
            sanitized_row[k] = v
        else:
            sanitized_row[k] = "***"
    return sanitized_row


def sanitize_result(result: Result) -> Result:
    """Sanitize a result for logging.

    Args:
        result: Query result to sanitize

    Returns:
        Sanitized result with sensitive values masked.
    """
    sanitized_result = result.copy()
    if "rows" in result:
        sanitized_result["rows"] = [sanitize_row(row) for row in result["rows"]]
    return sanitized_result


def log_query(query: str, parameters: Parameters = None) -> None:
    """Log a query execution.

    Args:
        query: SQL query to log
        parameters: Query parameters to log
    """
    logger.debug(
        "Executing query: %s with parameters: %s",
        sanitize_query(query),
        sanitize_parameters(parameters)
    )


def log_result(result: Union[Result, List[Row], Row]) -> None:
    """Log a query result.

    Args:
        result: Query result to log
    """
    if isinstance(result, dict) and "rows" in result:
        logger.debug(
            "Query result: %d rows, lastrowid: %s",
            len(result["rows"]),
            result.get("lastrowid")
        )
        sanitized_result = sanitize_result(result)
        logger.debug("Rows: %s", sanitized_result["rows"])
    else:
        logger.debug("Query result: %s", result)


def log_error(error: Exception, query: str, parameters: Parameters = None) -> None:
    """Log a query error.

    Args:
        error: Exception that occurred
        query: SQL query that failed
        parameters: Query parameters that failed
    """
    logger.error(
        "Error executing query: %s with parameters: %s: %s",
        sanitize_query(query),
        sanitize_parameters(parameters),
        str(error)
    ) 