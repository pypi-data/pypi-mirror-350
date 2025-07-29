import json
import os
from datetime import datetime

import pytest

from graph_builder.config import GraphBuilderConfig
from graph_builder.storage_manager import GraphBuilder


def test_get_now_timestamp():
    """Test that _get_now_timestamp returns a valid ISO format timestamp with Z suffix."""
    config = GraphBuilderConfig(output_dir="test_output")
    graph = GraphBuilder(config)

    # Get timestamp
    timestamp = graph._get_now_timestamp()

    # Verify format
    assert timestamp.endswith("Z")
    assert len(timestamp) > 0

    # Verify it's a valid ISO format
    try:
        parsed_time = datetime.fromisoformat(timestamp[:-1])  # Remove Z before parsing
        assert parsed_time is not None
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")


def test_add_entity():
    """Test that add_entity correctly writes to the entity log and updates the indexer."""
    # Setup
    config = GraphBuilderConfig(output_dir="test_output")
    graph = GraphBuilder(config)

    # Test data
    entity_id = 1
    properties = {"name": "Test Entity", "type": "test"}

    # Add entity
    graph.add_entity(entity_id, properties)

    # Verify log file exists and contains correct data
    assert os.path.exists(graph.entity_log_path)

    with open(graph.entity_log_path, encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1

        record = json.loads(lines[0])
        assert record["entity_id"] == entity_id
        assert record["properties"] == properties
        assert "update_time" in record
        assert record["update_time"].endswith("Z")

    # Cleanup
    os.remove(graph.entity_log_path)
    os.rmdir(os.path.dirname(graph.entity_log_path))


def test_add_relation():
    """Test that add_relation correctly writes to the relation log."""
    # Setup
    config = GraphBuilderConfig(output_dir="test_output")
    graph = GraphBuilder(config)

    # Test data
    relation_id = 100
    source_id = 1
    target_id = 2
    properties = {"type": "TEST_RELATION", "weight": 1.0}

    # Add relation
    graph.add_relation(relation_id, source_id, target_id, properties)

    # Verify log file exists and contains correct data
    assert os.path.exists(graph.relation_log_path)

    with open(graph.relation_log_path, encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1

        record = json.loads(lines[0])
        assert record["relation_id"] == relation_id
        assert record["source_id"] == source_id
        assert record["target_id"] == target_id
        assert record["properties"] == properties
        assert "update_time" in record
        assert record["update_time"].endswith("Z")
        graph.finalize()

    # Cleanup
    os.remove(graph.relation_log_path)
    os.rmdir(os.path.dirname(graph.relation_log_path))
