#!/usr/bin/env python3
"""A module for filtering logs."""
import os
import re
import logging
import mysql.connector
from typing import List, Tuple, Optional


# Define patterns for extracting and replacing PII data
patterns = {
    'extract': lambda fields, sep: r'(?P<field>{})=[^{}]*'.format('|'.join(fields), sep),
    'replace': lambda redaction: r'\g<field>={}'.format(redaction),
}

# Fields considered to contain Personally Identifiable Information (PII)
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Filters a log line to redact sensitive information."""
    extract_pattern = patterns["extract"](fields, separator)
    replace_pattern = patterns["replace"](redaction)
    return re.sub(extract_pattern, replace_pattern, message)


def get_logger() -> logging.Logger:
    """Creates and configures a logger for user data."""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to the database using environment variables."""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    
    return mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )


def main():
    """Logs information about user records from the database."""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            record = "; ".join(f"{col}={val}" for col, val in zip(columns, row))
            log_record = logging.LogRecord("user_data", logging.INFO, None, None, record, None, None)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to filter PII fields in log messages."""
    
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a LogRecord, redacting specified PII fields."""
        formatted_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, formatted_message, self.SEPARATOR)


if __name__ == "__main__":
    main()
