import os
from typing import Any

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


# Load environment variables (NEON_DATABASE_URL, etc.)
load_dotenv()

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("NEON_DATABASE_URL is not set. Please configure it in the environment.")


def get_db_connection() -> psycopg.Connection:
    """
    Returns a new Postgres connection to the Neon database.
    Uses dict_row so rows can be accessed by column name.
    """
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

