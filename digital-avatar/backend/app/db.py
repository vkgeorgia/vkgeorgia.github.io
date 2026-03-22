import os
import logging
from typing import Optional

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("NEON_DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("NEON_DATABASE_URL is not set. Please configure it in the environment.")

_pool: Optional[ConnectionPool] = None


def init_pool() -> None:
    """Open the connection pool. Call once at application startup (lifespan)."""
    global _pool
    _pool = ConnectionPool(
        DATABASE_URL,
        min_size=1,
        max_size=5,
        kwargs={"row_factory": dict_row},
    )
    logger.info("DB connection pool opened (min=1, max=5)")


def close_pool() -> None:
    """Close the pool gracefully. Call at application shutdown."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None
        logger.info("DB connection pool closed")


def get_pool() -> ConnectionPool:
    """Return the active pool. Raises if init_pool() was not called."""
    if _pool is None:
        raise RuntimeError("DB pool is not initialized. Call db.init_pool() first.")
    return _pool
