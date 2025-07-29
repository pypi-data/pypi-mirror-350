import json
import os
import tempfile

import pytest

from graph_builder.indexers import get_indexer
from graph_builder.indexers.memory_indexer import MemoryIndexer
from graph_builder.indexers.sqlite_indexer import SQLiteIndexer


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def test_get_indexer_memory(temp_dir):
    """Test getting a memory indexer."""
    indexer = get_indexer("memory", temp_dir)
    assert isinstance(indexer, MemoryIndexer)


def test_get_indexer_sqlite(temp_dir):
    """Test getting a SQLite indexer."""
    indexer = get_indexer("sqlite", temp_dir)
    assert isinstance(indexer, SQLiteIndexer)


def test_get_indexer_invalid_type(temp_dir):
    """Test getting an indexer with an invalid type."""
    with pytest.raises(ValueError, match="Unknown indexer type: invalid"):
        get_indexer("invalid", temp_dir)


def test_memory_indexer_add_entity(temp_dir):
    """Test adding an entity to the memory indexer."""
    indexer = MemoryIndexer(temp_dir)
    indexer.add_entity(1, {"name": "Test Entity"})
    assert indexer.map[1] == "Test Entity"


def test_memory_indexer_finalize(temp_dir):
    """Test finalizing the memory indexer."""
    indexer = MemoryIndexer(temp_dir)
    indexer.add_entity(1, {"name": "Test Entity"})
    indexer.finalize()

    # Check that the index file was created
    index_file = os.path.join(temp_dir, "memory_index.json")
    assert os.path.exists(index_file)

    # Check file content
    with open(index_file) as f:
        data = json.load(f)
        assert data == {"1": "Test Entity"}  # JSON serializes numbers as strings


def test_sqlite_indexer_add_entity(temp_dir):
    """Test adding an entity to the SQLite indexer."""
    indexer = SQLiteIndexer(temp_dir)
    indexer.add_entity(1, {"name": "Test Entity"})

    # Check that the entity was added to the database
    indexer.cursor.execute("SELECT name FROM entity_index WHERE entity_id = ?", (1,))
    result = indexer.cursor.fetchone()
    assert result[0] == "Test Entity"


def test_sqlite_indexer_finalize(temp_dir):
    """Test finalizing the SQLite indexer."""
    indexer = SQLiteIndexer(temp_dir)
    indexer.add_entity(1, {"name": "Test Entity"})
    indexer.finalize()

    # Check that the database file was created
    db_file = os.path.join(temp_dir, "index.db")
    assert os.path.exists(db_file)

    # Try to connect to the database to verify it's valid
    import sqlite3

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM entity_index WHERE entity_id = ?", (1,))
    result = cursor.fetchone()
    assert result[0] == "Test Entity"
    conn.close()


def test_sqlite_indexer_update_entity(temp_dir):
    """Test updating an existing entity in the SQLite indexer."""
    indexer = SQLiteIndexer(temp_dir)

    # Add initial entity
    indexer.add_entity(1, {"name": "Initial Name"})

    # Update the entity
    indexer.add_entity(1, {"name": "Updated Name"})

    # Check that the entity was updated
    indexer.cursor.execute("SELECT name FROM entity_index WHERE entity_id = ?", (1,))
    result = indexer.cursor.fetchone()
    assert result[0] == "Updated Name"
