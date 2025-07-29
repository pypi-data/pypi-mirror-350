"""
Module for persistent database operations.

This module provides a persistent database implementation using diskcache for various application data.
It offers a thread-safe, key-value storage system with support for MongoDB-style querying,
including conditions, projections, sorting, and pagination.
The module defines two main classes:
1. Query: A utility class for constructing MongoDB-style query operators.
2. DataBase: The core class implementing the persistent database functionality.

Key features:
- Singleton instances for different data types
- Thread-safe operations using locks
- Support for adding, updating, retrieving, and removing data
- Advanced querying capabilities with MongoDB-style syntax
- Sorting and pagination support
- Data persistence across application restarts

Usage:
    from diskcachedb.db import DiskDB

    # Get a database instance
    db = DiskDB()

    # Add data
    db.add("key1", {"foo": "bar", "status": "pending", "priority": 1})

    # Query data - Example 1: Complex query with AND, OR, and comparison operators
    results = db.query(
        conditions={
            "$and": [
                {"status": "pending"},
                {"$or": [
                    {"priority": {"$gt": 0}},
                    {"priority": 0}
                ]},
                {"files": {"$exists": True}},
                {"issue_number": {"$nin": ["1234", "5678"]}},
                {"foo": "bar"}
            ]
        },
        sort=[("priority", -1), ("created_at", 1)],
        limit=10
    )

    # Query data - Example 2: Simple OR condition with projection
    results = db.query(
        conditions={
            "$or": [
                {"status": "failed"},
                {"status": "pending"}
            ]
        },
        projection={"issue_number": 1, "task_id": 1, "status": 1, "files": 1},
        sort={"_added_at": -1},
        limit=20
    )

    print(results)

This module is designed to provide a flexible and efficient data storage solution
for various components of the application, ensuring data persistence and
offering powerful querying capabilities.
"""

from diskcache import Cache
from typing import Any, Dict, List, Optional, Union
from threading import Lock, RLock
from pathlib import Path
from bson.objectid import ObjectId
from datetime import datetime
from logging import getLogger, StreamHandler, Formatter

logger = getLogger('diskcachedb')
logger.setLevel('DEBUG')
formatter = Formatter(
    "%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s:%(lineno)d %(funcName)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler = StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


class DiskDB:
    """Persistent data base using diskcache for various application data.

    A MongoDB-like interface for disk-based caching using diskcache.
    """

    _instances: Dict[str, 'DiskDB'] = {}
    _instances_lock = Lock()  # Lock for singleton instance creation

    def __init__(self, name: str, base_directory: Union[str, Path] = None):
        """
        Initialize the database with a directory for storage.

        Args:
            name: Name of the database instance
            base_directory: Path to the directory where the cache will be stored
        """
        self.name = name
        if base_directory is None:
            base_directory = Path.home() / ".diskcache"
        elif isinstance(base_directory, str):
            base_directory = Path(base_directory)

        # Ensure directories exist
        base_directory.mkdir(parents=True, exist_ok=True)
        self._cache_dir = base_directory / name
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = Cache(str(self._cache_dir))  # Cache expects string path

        self.list_key = f'{name}_list'
        self.key_prefix = name
        self._key_counter = 0  # For sequential keys
        self._lock = RLock()  # Reentrant lock for thread safety
        # Initialize list if not exists
        with self._lock:
            if self.list_key not in self.cache:
                self.cache.set(self.list_key, [])

    def add(self, data: Any) -> str:
        """Add data to base with auto-generated ObjectId.
        Args:
            data: Data to store (must be JSON serializable)
        Returns:
            str: ObjectId of the inserted document
        """
        with self._lock:
            # Convert to dict if needed
            if hasattr(data, '__dict__'):
                data_dict = data.__dict__.copy()
            else:
                data_dict = data.copy() if isinstance(
                    data, dict) else {'value': data}
            # Generate new ObjectId
            _id = str(ObjectId())
            # Add MongoDB-style metadata
            if isinstance(data_dict, dict):
                data_dict['_id'] = _id
                # Use MongoDB-style timestamps
                now = datetime.now()
                data_dict['created_at'] = now
                data_dict['last_updated_at'] = now
            # Store data
            self.cache.set(_id, data_dict)
            # Add to list
            items = self.cache.get(self.list_key, [])
            if _id not in items:
                items.append(_id)
                self.cache.set(self.list_key, items)
            logger.debug(f"Inserted document with _id: {_id}")
            return _id

    def get(self, key: str) -> Optional[Any]:
        """Get data from database.
        Args:
            key: ObjectId of data to retrieve
        Returns:
            Data if found, None otherwise
        """
        with self._lock:
            return self.cache.get(key)

    def update(self, key: str, data: Any, upsert: bool = True) -> bool:
        """Update existing data atomically.
        This method performs an atomic update by:
        1. Getting existing data
        2. Merging new data with existing data
        3. Preserving metadata fields
        4. Updating timestamp and thread info
        Args:
            key: ObjectId of data to update
            data: New data (must be JSON serializable)
            upsert: If True, will create new item if it doesn't exist
        Returns:
            bool: True if update was successful, False if key doesn't exist
        """
        with self._lock:
            # Get existing data first
            existing = self.cache.get(key)
            if existing is None:
                if not upsert:
                    return False
                else:
                    self.add(key, data)
                    return True
            # Convert input to dict if needed
            if hasattr(data, '__dict__'):
                update_dict = data.__dict__
            else:
                update_dict = data
            # Preserve existing data and metadata
            result_dict = existing.copy()
            result_dict.update(update_dict)  # Update with new data
            # Update metadata
            result_dict['last_updated_at'] = datetime.now()
            # Atomic set
            self.cache.set(key, result_dict)
            logger.debug(f"Updated item {key}")
            return True

    def remove(self, key: str) -> None:
        """Remove data from database.
        Args:
            key: ObjectId of data to remove
        """
        with self._lock:
            self.cache.delete(key)
            items = self.cache.get(self.list_key, [])
            if key in items:
                items.remove(key)
                self.cache.set(self.list_key, items)
            logger.debug(f"Removed item {key}")

    def get_all(self) -> List[Any]:
        """Get all items in database."""
        with self._lock:
            items = []
            for key in self.cache.get(self.list_key, []):
                item = self.cache.get(key)
                if item is not None:
                    items.append(item)
            return items

    def _match_condition(self, item: Dict, condition: Dict) -> bool:
        """Check if item matches a query condition using MongoDB-style operators.
        Args:
            item: Item to check
            condition: Query condition using MongoDB operators
        Returns:
            True if item matches condition
        """
        for field, operators in condition.items():
            if field == "$and":
                return all(self._match_condition(item, cond) for cond in operators)
            elif field == "$or":
                return any(self._match_condition(item, cond) for cond in operators)
            if not isinstance(operators, dict):
                # Direct value comparison
                if field not in item or item[field] != operators:
                    return False
                continue
            value = item.get(field)
            if value is None:
                return False
            for op, target in operators.items():
                if op == "$eq":
                    if value != target:
                        return False
                elif op == "$ne":
                    if value == target:
                        return False
                elif op == "$gt":
                    if not value > target:
                        return False
                elif op == "$gte":
                    if not value >= target:
                        return False
                elif op == "$lt":
                    if not value < target:
                        return False
                elif op == "$lte":
                    if not value <= target:
                        return False
                elif op == "$in":
                    if value not in target:
                        return False
                elif op == "$nin":
                    if value in target:
                        return False
            for op, target in operators.items():
                if op == "$eq" and value != target:
                    return False
                elif op == "$ne" and value == target:
                    return False
                elif op == "$gt" and not value > target:
                    return False
                elif op == "$gte" and not value >= target:
                    return False
                elif op == "$lt" and not value < target:
                    return False
                elif op == "$lte" and not value <= target:
                    return False
                elif op == "$in" and value not in target:
                    return False
                elif op == "$nin" and value in target:
                    return False
                elif op == "$exists" and (target and field not in item or not target and field in item):
                    return False
        return True

    def _apply_projection(self, item: Dict, projection: Dict) -> Dict:
        """Apply projection to an item.
        Args:
            item: Item to project
            projection: Projection specification
                Examples:
                - {"field1": 1, "field2": 1} # Include only field1 and field2
                - {"field1": 0, "field2": 0} # Exclude field1 and field2
        Returns:
            Projected item
        """
        if not projection:
            return item
        # Check if we're in inclusion or exclusion mode
        includes = any(v == 1 for v in projection.values())
        excludes = any(v == 0 for v in projection.values())
        if includes and excludes:
            raise ValueError("Cannot mix inclusive and exclusive projections")
        result = {}
        if includes:
            # Inclusion mode: only include specified fields
            for field, value in projection.items():
                if value == 1 and field in item:
                    result[field] = item[field]
        else:
            # Exclusion mode: include all except specified fields
            for field, value in item.items():
                if field not in projection or projection[field] != 0:
                    result[field] = value
        return result

    def _apply_sort(self, items: List[Dict], sort_spec: Dict) -> List[Dict]:
        """Sort items based on sort specification.
        Args:
            items: Items to sort
            sort_spec: Sort specification
                Examples:
                - {"created_at": 1}  # Ascending
                - {"priority": -1}   # Descending
                - {"status": 1, "created_at": -1}  # Multi-field
        Returns:
            Sorted items
        """
        if not sort_spec:
            return items

        def get_sort_key(item):
            # Build tuple of sort keys
            keys = []
            for field, direction in sort_spec.items():
                value = item.get(field)
                # Handle None values
                if value is None:
                    value = datetime.min if isinstance(
                        value, datetime) else float('-inf')
                # For descending order, we need to invert the sort key
                # For datetime, we can negate the timestamp
                if direction == -1:
                    if isinstance(value, datetime):
                        value = datetime.max - value
                    else:
                        value = (value, True)  # True sorts after False
                keys.append(value)
            return tuple(keys)
        return sorted(items, key=get_sort_key)

    def query(
        self,
        conditions: Union[Dict, None] = None,
        projection: Union[Dict, None] = None,
        sort: Union[Dict, None] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[Any]:
        """Query items using MongoDB-style conditions, projections, and sorting.
        Args:
            conditions: Query conditions (MongoDB-style)
                Examples:
                - {"status": "pending"} # Direct equality
                - {"status": {"$eq": "pending"}} # Explicit equality
                - {"created_at": {"$gt": "2023-01-01"}} # Greater than
                - {"$and": [                        # Logical AND
                    {"status": "pending"},
                    {"created_at": {"$gt": "2023-01-01"}}
                  ]}
                - {"$or": [                         # Logical OR
                    {"status": "pending"},
                    {"status": "processing"}
                  ]}
                - {"priority": {"$in": [1, 2, 3]}} # In array
                - {"count": {"$gte": 5}}          # Greater than or equal
            projection: Fields to include/exclude (MongoDB-style)
                Examples:
                - {"key1": 1, "key2": 1} # Only include key1 and key2
                - {"key3": 0} # Exclude key3
            sort: Sort specification (MongoDB-style)
                Examples:
                - {"key1": 1}  # Ascending by key1
                - {"key2": -1}   # Descending by key2
                - {"status": 1, "created_at": -1}  # Multi-field sort
            limit: Maximum number of items to return
            skip: Number of items to skip
        Returns:
            List of matching items with projected fields
        """
        with self._lock:
            items = self.get_all()
            if not any([conditions, projection, sort, limit, skip]):
                return items
            # Apply conditions
            if conditions:
                items = [
                    item for item in items
                    if self._match_condition(item, conditions)
                ]
            # Apply sort
            if sort:
                items = self._apply_sort(items, sort)
            # Apply skip and limit
            if skip:
                items = items[skip:]
            if limit:
                items = items[:limit]
            # Apply projection
            if projection:
                items = [
                    self._apply_projection(item, projection)
                    for item in items
                ]
            return items

    def clear(self) -> None:
        """Clear all data from database."""
        with self._lock:
            for key in self.cache.get(self.list_key, []):
                self.cache.delete(key)
            self.cache.set(self.list_key, [])
            logger.info("Cleared all items from database")

    def __enter__(self):
        """Context manager entry."""
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._lock.release()


if __name__ == "__main__":
    db = DiskDB('test')

    # Insert a document
    doc = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
    _id = db.add(doc)
    logger.debug(f"Inserted document with _id: {_id}")
    # Retrieve the document
    result = db.get(_id)
    logger.debug(f"Retrieved document: {result}")
    # Update document
    db.update(_id, {"key2": "value2_updated"})
    logger.debug(f"Updated document: {db.get(_id)}")
    # Insert a simple document
    _id2 = db.add({"key1": "value1"})
    logger.debug(f"Inserted document with _id: {_id2}")
    # Retrieve the document
    result2 = db.get(_id2)
    logger.debug(f"Retrieved document: {result2}")
    # Update document
    db.update(_id2, {"key1": "value1_updated"})
    logger.debug(f"Updated document: {db.get(_id2)}")
    # Remove document
    db.remove(_id2)
    logger.debug(f"Removed document: {_id2}")
    # Clear all documents
    db.clear()
    logger.debug("Cleared all documents")
