import json
import os
import tempfile

import pytest

from graph_builder.compactor import GraphCompactor
from graph_builder.config import GraphBuilderConfig
from graph_builder.storage_manager import GraphBuilder
from tests.fixture_generator import create_test_graph_fixture


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def graph_builder(temp_dir):
    """Create a GraphBuilder instance with a temporary directory."""
    config = GraphBuilderConfig(output_dir=temp_dir)
    return GraphBuilder(config)


@pytest.fixture
def compactor(temp_dir):
    """Create a GraphCompactor instance with a temporary directory."""
    return GraphCompactor(base_dir=temp_dir)


def test_compactor_initialization(temp_dir):
    """Test that the compactor creates necessary directories."""
    GraphCompactor(base_dir=temp_dir)

    # Check that directories are created
    assert os.path.exists(os.path.join(temp_dir, "entities"))
    assert os.path.exists(os.path.join(temp_dir, "adjacency"))


def test_compact_entities_empty_log(temp_dir, compactor):
    """Test compacting entities with an empty log file."""
    # Create empty log file
    os.makedirs(os.path.join(temp_dir, "logs"), exist_ok=True)
    # Create an empty file and close it immediately
    open(os.path.join(temp_dir, "logs", "entity_updates.jsonl"), "w").close()

    # Run compaction after file is created and closed
    compactor.compact_entities()

    # Check that no shard files were created
    assert len(os.listdir(os.path.join(temp_dir, "entities"))) == 0


def test_compact_entities_single_update(temp_dir, graph_builder, compactor):
    """Test compacting entities with a single update."""
    # Add an entity
    graph_builder.add_entity(1, {"name": "Test Entity"})

    # Run compaction
    compactor.compact_entities()

    # Check that a shard file was created
    shard_files = os.listdir(os.path.join(temp_dir, "entities"))
    assert len(shard_files) == 1

    # Check shard content
    with open(os.path.join(temp_dir, "entities", shard_files[0])) as f:
        records = [json.loads(line) for line in f]
        assert len(records) == 1
        assert records[0]["entity_id"] == 1
        assert records[0]["properties"] == {"name": "Test Entity"}


def test_compact_entities_multiple_updates(temp_dir, graph_builder, compactor):
    """Test compacting entities with multiple updates to the same entity."""
    # Add multiple updates to the same entity
    graph_builder.add_entity(1, {"name": "Test Entity"})
    graph_builder.add_entity(1, {"email": "test@example.com"})
    graph_builder.add_entity(1, {"age": 30})

    # Run compaction
    compactor.compact_entities()

    # Check that a shard file was created
    shard_files = os.listdir(os.path.join(temp_dir, "entities"))
    assert len(shard_files) == 1

    # Check shard content
    with open(os.path.join(temp_dir, "entities", shard_files[0])) as f:
        records = [json.loads(line) for line in f]
        assert len(records) == 1
        assert records[0]["entity_id"] == 1
        assert records[0]["properties"] == {
            "name": "Test Entity",
            "email": "test@example.com",
            "age": 30,
        }


def test_compact_entities_sharding(temp_dir, graph_builder, compactor):
    """Test that entities are properly sharded when exceeding shard size."""
    # Set a small shard size
    compactor.shard_size = 2

    # Add multiple entities
    for i in range(5):
        graph_builder.add_entity(i, {"name": f"Entity {i}"})

    # Run compaction
    compactor.compact_entities()

    # Check that multiple shard files were created
    shard_files = os.listdir(os.path.join(temp_dir, "entities"))
    assert len(shard_files) == 3  # 5 entities with shard_size=2 should create 3 shards

    # Check total number of records across all shards
    total_records = 0
    for shard_file in shard_files:
        with open(os.path.join(temp_dir, "entities", shard_file)) as f:
            total_records += len([json.loads(line) for line in f])
    assert total_records == 5


def test_build_adjacency_empty_log(temp_dir, compactor):
    """Test building adjacency list with an empty log file."""
    # Create empty log file
    os.makedirs(os.path.join(temp_dir, "logs"), exist_ok=True)
    with open(os.path.join(temp_dir, "logs", "relation_updates.jsonl"), "w") as f:
        pass

    # Run adjacency building
    compactor.build_adjacency()

    # Check that adjacency file was created but is empty
    assert os.path.exists(os.path.join(temp_dir, "adjacency", "adjacency.jsonl"))
    with open(os.path.join(temp_dir, "adjacency", "adjacency.jsonl")) as f:
        assert len(f.readlines()) == 0


def test_build_adjacency_single_relation(temp_dir, graph_builder, compactor):
    """Test building adjacency list with a single relation."""
    # Add a relation
    graph_builder.add_relation(1, 1, 2, {"type": "FRIEND"})

    # Run adjacency building
    compactor.build_adjacency()

    # Check adjacency file content
    with open(os.path.join(temp_dir, "adjacency", "adjacency.jsonl")) as f:
        records = [json.loads(line) for line in f]
        assert len(records) == 1
        assert records[0]["entity_id"] == 1
        assert records[0]["relations"] == [1]


def test_build_adjacency_multiple_relations(temp_dir, graph_builder, compactor):
    """Test building adjacency list with multiple relations."""
    # Add multiple relations
    graph_builder.add_relation(1, 1, 2, {"type": "FRIEND"})
    graph_builder.add_relation(2, 1, 3, {"type": "FAMILY"})
    graph_builder.add_relation(3, 2, 3, {"type": "COLLEAGUE"})

    # Run adjacency building
    compactor.build_adjacency()

    # Check adjacency file content
    with open(os.path.join(temp_dir, "adjacency", "adjacency.jsonl")) as f:
        records = {
            r["entity_id"]: r["relations"] for r in [json.loads(line) for line in f]
        }
        assert records[1] == [1, 2]  # Entity 1 has relations 1 and 2
        assert records[2] == [3]  # Entity 2 has relation 3


def test_integration_compactor_with_fixture_data():
    """Integration test using fixture data to verify compaction process."""
    # Create test fixture data
    test_dir = create_test_graph_fixture("test_integration_graph")
    try:
        # Remove the pre-compacted files to force actual compaction
        import shutil

        shutil.rmtree(os.path.join(test_dir, "entities"))
        shutil.rmtree(os.path.join(test_dir, "relations"))
        shutil.rmtree(os.path.join(test_dir, "adjacency"))

        # Initialize compactor with test data
        compactor = GraphCompactor(base_dir=test_dir)

        # Run compaction operations
        compactor.compact_entities()
        compactor.compact_relations()
        compactor.build_adjacency()

        # Verify compacted entities
        with open(os.path.join(test_dir, "entities", "shard_00000.jsonl")) as f:
            entities = [json.loads(line) for line in f]

        # Verify specific entity updates were merged correctly
        alice = next(e for e in entities if e["entity_id"] == 1)
        assert alice["properties"] == {
            "name": "Alice",
            "type": "Person",
            "email": "alice@example.com",
        }
        assert alice["last_update_time"] == "2025-04-28T12:05:00Z"

        bob = next(e for e in entities if e["entity_id"] == 2)
        assert bob["properties"] == {"name": "Bobby", "type": "Person"}
        assert bob["last_update_time"] == "2025-04-28T12:06:00Z"

        # Verify relations are properly compacted
        with open(os.path.join(test_dir, "relations", "shard_0.jsonl")) as f:
            relations = [json.loads(line) for line in f]

        # Verify specific relations
        friend_relation = next(r for r in relations if r["relation_id"] == 101)
        assert friend_relation["source_id"] == 1
        assert friend_relation["target_id"] == 2
        assert friend_relation["properties"] == {"type": "FRIENDS_WITH"}
        assert friend_relation["update_time"] == "2025-04-28T12:10:00Z"

        coworker_relation = next(r for r in relations if r["relation_id"] == 102)
        assert coworker_relation["source_id"] == 2
        assert coworker_relation["target_id"] == 3
        assert coworker_relation["properties"] == {"type": "COWORKERS_WITH"}
        assert coworker_relation["update_time"] == "2025-04-28T12:12:00Z"

        # Verify adjacency list
        with open(os.path.join(test_dir, "adjacency", "adjacency.jsonl")) as f:
            adjacency = [json.loads(line) for line in f]

        # Verify relations are correctly mapped
        entity1_adj = next(a for a in adjacency if a["entity_id"] == 1)
        assert entity1_adj["relations"] == [101]  # Alice -> Bob relation

        entity2_adj = next(a for a in adjacency if a["entity_id"] == 2)
        assert entity2_adj["relations"] == [102]  # Bob -> Charlie relation

    finally:
        # Cleanup test directory
        if os.path.exists(test_dir):
            import shutil

            shutil.rmtree(test_dir)
