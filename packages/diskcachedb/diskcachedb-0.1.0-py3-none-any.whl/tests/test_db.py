"""
Tests for the DiskDB class.

This module contains comprehensive tests for the DiskDB class, covering:
- Basic CRUD operations
- Complex queries
- Thread safety
- Metadata handling
- Projections and sorting
"""

import pytest
from diskcachedb import DiskDB
import tempfile
import shutil
import os
from datetime import datetime
from threading import Thread
import time
import random

@pytest.fixture
def db():
    """Create a temporary database for testing."""
    temp_dir = tempfile.mkdtemp()
    test_db = DiskDB('test', temp_dir)
    yield test_db
    shutil.rmtree(temp_dir)  # cleanup after test

@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'status': 'active',
            'score': 95,
            'tags': ['premium', 'verified'],
            'created_at': datetime(2025, 1, 1)
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'status': 'pending',
            'score': 85,
            'tags': ['basic'],
            'created_at': datetime(2025, 1, 2)
        },
        {
            'name': 'Bob Wilson',
            'email': 'bob@example.com',
            'status': 'inactive',
            'score': 75,
            'created_at': datetime(2025, 1, 3)
        }
    ]

def test_add_and_get(db):
    """Test basic add and get operations."""
    # Test adding a simple document
    doc = {'name': 'Test User', 'score': 100}
    doc_id = db.add(doc)

    # Verify the document was added
    assert doc_id is not None
    retrieved = db.get(doc_id)
    assert retrieved['name'] == 'Test User'
    assert retrieved['score'] == 100

    # Verify metadata fields
    assert '_id' in retrieved
    assert 'created_at' in retrieved
    assert 'last_updated_at' in retrieved

def test_update(db):
    """Test update operations."""
    # Add initial document
    doc_id = db.add({'status': 'pending', 'count': 0})

    # Test update with new field
    db.update(doc_id, {'status': 'active', 'priority': 'high'})
    updated = db.get(doc_id)
    assert updated['status'] == 'active'
    assert updated['priority'] == 'high'
    assert updated['count'] == 0  # Original field should remain

    # Test update timestamp
    original_update_time = updated['last_updated_at']
    time.sleep(0.1)  # Ensure timestamp difference
    db.update(doc_id, {'count': 1})
    re_updated = db.get(doc_id)
    assert re_updated['last_updated_at'] > original_update_time

def test_remove(db, sample_data):
    """Test remove operations."""
    # Add and remove a document
    doc_id = db.add(sample_data[0])
    assert db.get(doc_id) is not None
    db.remove(doc_id)
    assert db.get(doc_id) is None

    # Verify it's removed from the list
    all_items = db.get_all()
    assert not any(item.get('_id') == doc_id for item in all_items)

def test_query_conditions(db, sample_data):
    """Test query conditions."""
    # Add sample data
    for doc in sample_data:
        db.add(doc)

    # Test simple equality
    results = db.query(conditions={'status': 'active'})
    assert len(results) == 1
    assert results[0]['name'] == 'John Doe'

    # Test complex AND query
    results = db.query(conditions={
        '$and': [
            {'score': {'$gt': 80}},
            {'tags': {'$exists': True}},
        ]
    })
    assert len(results) == 2

    # Test OR query with IN operator
    results = db.query(conditions={
        '$or': [
            {'status': {'$in': ['pending', 'inactive']}},
            {'score': {'$gte': 95}}
        ]
    })
    assert len(results) == 3

def test_query_projection(db, sample_data):
    """Test query projections."""
    # Add sample data
    for doc in sample_data:
        db.add(doc)

    # Test inclusion projection
    results = db.query(
        conditions={'score': {'$gt': 80}},
        projection={'name': 1, 'score': 1}
    )
    assert len(results) == 2
    assert set(results[0].keys()) == {'name', 'score'}

    # Test exclusion projection
    results = db.query(
        conditions={'status': 'active'},
        projection={'tags': 0, 'created_at': 0}
    )
    assert 'tags' not in results[0]
    assert 'created_at' not in results[0]

def test_query_sort_and_limit(db, sample_data):
    """Test sorting and pagination."""
    # Add sample data
    for doc in sample_data:
        db.add(doc)

    # Test sorting
    results = db.query(
        sort={'score': -1}  # Descending
    )
    assert len(results) == 3
    assert results[0]['score'] == 95
    assert results[-1]['score'] == 75

    # Test limit and skip
    results = db.query(
        sort={'created_at': 1},
        limit=2,
        skip=1
    )
    assert len(results) == 2
    assert results[0]['name'] == 'Jane Smith'

def test_thread_safety(db):
    """Test thread safety of operations."""
    def worker(worker_id):
        for _ in range(50):
            doc = {'worker': worker_id, 'value': random.randint(1, 100)}
            db.add(doc)
            time.sleep(0.01)  # Simulate work

    # Create and start threads
    threads = [Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Verify results
    all_items = db.get_all()
    assert len(all_items) == 250  # 5 threads * 50 documents each
    worker_counts = {}
    for item in all_items:
        worker_counts[item['worker']] = worker_counts.get(item['worker'], 0) + 1

    # Verify each worker added exactly 50 documents
    for worker_id in range(5):
        assert worker_counts[worker_id] == 50

def test_clear(db, sample_data):
    """Test clearing the database."""
    # Add sample data
    for doc in sample_data:
        db.add(doc)

    # Verify data exists
    assert len(db.get_all()) == len(sample_data)

    # Clear the database
    db.clear()

    # Verify all data is removed
    assert len(db.get_all()) == 0
