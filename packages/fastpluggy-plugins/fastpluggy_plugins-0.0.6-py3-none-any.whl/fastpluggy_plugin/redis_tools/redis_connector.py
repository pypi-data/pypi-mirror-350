from typing import List, Dict, Any

import redis
from fastapi import HTTPException

from .schema import RedisKey

import pickle

def try_unpickle(value_data):
    """
    Try to detect and decode pickled data safely.
    Returns:
        - Tuple (is_pickled: bool, value: Any)
    """
    if not value_data:
        return False, value_data

    # Make sure it's bytes
    if isinstance(value_data, str):
        try:
            value_data = value_data.encode('utf-8')
        except Exception:
            return False, value_data

    try:
        # Try to unpickle
        value = pickle.loads(value_data)
        return True, value
    except (pickle.UnpicklingError, EOFError, AttributeError, ValueError, TypeError):
        return False, value_data

class RedisConnection:
    def __init__(self, db: int = None):
        # Get settings from config
        from .config import RedisToolsSettings
        self.settings = RedisToolsSettings()

        # Use provided db or default from settings
        db_to_use = db if db is not None else self.settings.redis_db

        # Create Redis client with settings
        self.client = self._create_client(db_to_use)

    def _create_client(self, db: int = 0) -> redis.Redis:
        if self.settings.REDIS_DSN:
            return redis.from_url(
                self.settings.REDIS_DSN,
                db=db,
                decode_responses=self.settings.redis_decode_responses
            )
        return redis.Redis(
            host=self.settings.redis_host,
            port=self.settings.redis_port,
            ssl=self.settings.use_ssl,
            db=db,
            password=self.settings.redis_password,
            decode_responses=self.settings.redis_decode_responses
        )

    def test_connection(self) -> bool:
        try:
            return self.client.ping()
        except redis.exceptions.ConnectionError:
            return False

    def get_key_details(self, key: str, preview_mode: bool = False) -> RedisKey:
        """
        Helper method to get key details from Redis.

        Args:
            key: The Redis key to get details for
            preview_mode: If True, returns a preview of the data instead of the full value

        Returns:
            A RedisKey object with key details
        """
        key_type = self.client.type(key)
        if type(key_type) is bytes:
            key_type = key_type.decode('utf-8')
        ttl = self.client.ttl(key)
        value = None
        size = None
        preview = None

        # Get size and data based on key type
        if key_type == "string":
            value_data = self.client.get(key)
            size = len(value_data) if value_data else 0

            is_pickled, decoded_value = try_unpickle(value_data)

            if preview_mode:
                preview = str(decoded_value)[:100] if decoded_value else ""
            else:
                value = str(decoded_value)
        elif key_type == "list":
            size = self.client.llen(key)
            if preview_mode:
                preview = str(self.client.lrange(key, 0, 5))
            else:
                value = self.client.lrange(key, 0, -1)
        elif key_type == "hash":
            size = self.client.hlen(key)
            hash_data = self.client.hgetall(key)
            if preview_mode:
                preview = str(dict(list(hash_data.items())[:5]))
            else:
                value = hash_data
        elif key_type == "set":
            size = self.client.scard(key)
            set_data = self.client.smembers(key)
            if preview_mode:
                preview = str(list(set_data)[:5])
            else:
                value = list(set_data)
        elif key_type == "zset":
            size = self.client.zcard(key)
            if preview_mode:
                preview = str(self.client.zrange(key, 0, 5, withscores=True))
            else:
                value = self.client.zrange(key, 0, -1, withscores=True)

        # Create and return RedisKey with appropriate fields
        return RedisKey(
            key=key,
            type=key_type,
            ttl=ttl,
            size=size,
            preview=preview if preview_mode else None,
            value=value if not preview_mode else None
        )

    # def get_key_info(self, key: str) -> RedisKey:
    #     """
    #     Get preview information about a Redis key.
    #
    #     Args:
    #         key: The Redis key to get information for
    #
    #     Returns:
    #         RedisKey object with preview data
    #     """
    #     return self.get_key_details(key, preview_mode=True)

    def get_keys(self, pattern: str = "*", limit: int = None) -> List[RedisKey]:
        """
        Get a list of keys matching the pattern with their info.

        Args:
            pattern: Redis key pattern to match
            limit: Maximum number of keys to return, defaults to settings.keys_limit

        Returns:
            List of RedisKey objects with preview data
        """
        # Use provided limit or default from settings
        if limit is None:
            limit = self.settings.keys_limit

        keys = self.client.keys(pattern)[:limit]
        return [self.get_key_details(key, preview_mode=True) for key in keys]

    # def get_key_data(self, key: str) -> RedisKey:
    #     """
    #     Get full data for a Redis key.
    #
    #     Args:
    #         key: The Redis key to get data for
    #
    #     Returns:
    #         RedisKey object with full value data
    #     """
    #     return self.get_key_details(key, preview_mode=False)

    def delete_key(self, key: str) -> bool:
        return bool(self.client.delete(key))

    def flush_db(self) -> bool:
        self.client.flushdb()
        return True

    def get_current_db(self) -> int:
        """Get the current database index."""
        return self.client.connection_pool.connection_kwargs.get('db', 0)

    def get_databases(self) -> List[Dict[str, Any]]:
        """Get a list of available Redis databases with key counts."""
        # Create a connection to database 0 to run the INFO command
        info_client = self._create_client(0)

        # Get database info from Redis INFO command
        info = info_client.info('keyspace')

        # Default Redis has 16 databases (0-15)
        # We can determine the actual number from the keyspace info
        max_db = 15  # Default max database index

        # Find the highest database index in the keyspace info
        for key in info.keys():
            if key.startswith('db'):
                try:
                    db_index = int(key[2:])  # Extract number from 'db0', 'db1', etc.
                    max_db = max(max_db, db_index)
                except ValueError:
                    pass

        # Create a list of all databases (even empty ones)
        databases = []
        current_db = self.get_current_db()

        for i in range(max_db + 1):
            db_key = f'db{i}'
            db_info = info.get(db_key, {})

            # If the database isn't in the info, it's empty
            keys = db_info.get('keys', 0)
            expires = db_info.get('expires', 0)

            databases.append({
                'index': i,
                'keys': keys,
                'expires': expires,
                'current': i == current_db
            })

        return databases

    def select_db(self, db_index: int) -> bool:
        try:
            self.client = self._create_client(db_index)
            self.db = db_index
            return self.test_connection()
        except Exception:
            return False


def get_redis_connection(db: int = None):
    conn = RedisConnection(db=db)
    if not conn.test_connection():
        raise HTTPException(status_code=500, detail="Cannot connect to Redis server")
    return conn
