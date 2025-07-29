import json
import os

from fixture_generator import create_test_graph_fixture

from graph_builder.compactor import GraphCompactor


def test_integration_compactor_with_fixture_data():
    """Integration test using fixture data to verify compaction process."""
    # Create test fixture data
    test_dir = create_test_graph_fixture("test_integration_graph")
    try:
        # Initialize compactor with test data
        compactor = GraphCompactor(base_dir=test_dir)

        # Run compaction operations
        compactor.compact_entities()
        compactor.build_adjacency()

        # Verify compacted entities
        with open(os.path.join(test_dir, "entities", "shard_0.jsonl")) as f:
            entities = [json.loads(line) for line in f]

        # Verify specific entity updates were merged correctly
        alice = next(e for e in entities if e["entity_id"] == 1)
        assert alice["properties"] == {
            "name": "Alice",
            "type": "Person",
            "email": "alice@example.com",
            "community_id": "team_alpha",
        }
        assert alice["last_update_time"] == "2025-04-28T12:05:00Z"

        bob = next(e for e in entities if e["entity_id"] == 2)
        assert bob["properties"]["name"] == "Bobby"  # Verify name was updated
        assert bob["last_update_time"] == "2025-04-28T12:06:00Z"

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
