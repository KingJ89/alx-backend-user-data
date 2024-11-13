#!/usr/bin/env python3
"""
Main file to test RedactingFormatter
"""

import logging

# Import RedactingFormatter from filtered_logger module
RedactingFormatter = __import__('filtered_logger').RedactingFormatter

# Define a test log message containing sensitive information
message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord(
    name="my_logger",
    level=logging.INFO,
    pathname=None,
    lineno=None,
    msg=message,
    args=None,
    exc_info=None
)

# Initialize formatter to redact specific fields
formatter = RedactingFormatter(fields=("email", "ssn", "password"))

# Print the formatted log record with PII redacted
print(formatter.format(log_record))
