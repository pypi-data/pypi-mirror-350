import json
import os


def create_test_graph_fixture(base_dir="test_graph_fixture"):
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "entities"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "relations"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "adjacency"), exist_ok=True)

    # Logs: multiple updates for compactor testing
    entity_logs = [
        {
            "entity_id": 1,
            "properties": {"name": "Alice", "type": "Person"},
            "update_time": "2025-04-28T12:00:00Z",
        },
        {
            "entity_id": 1,
            "properties": {"email": "alice@example.com"},
            "update_time": "2025-04-28T12:05:00Z",
        },
        {
            "entity_id": 2,
            "properties": {"name": "Bob", "type": "Person"},
            "update_time": "2025-04-28T12:01:00Z",
        },
        {
            "entity_id": 2,
            "properties": {"name": "Bobby"},
            "update_time": "2025-04-28T12:06:00Z",
        },
        {
            "entity_id": 3,
            "properties": {
                "name": "Charlie",
                "type": "Person",
                "community_id": "team_beta",
            },
            "update_time": "2025-04-28T12:02:00Z",
        },
    ]
    with open(
        os.path.join(base_dir, "logs", "entity_updates.jsonl"), "w", encoding="utf-8"
    ) as f:
        for record in entity_logs:
            f.write(json.dumps(record) + "\n")

    # Logs: relations (no changes needed here for now)
    relation_logs = [
        {
            "relation_id": 101,
            "source_id": 1,
            "target_id": 2,
            "properties": {"type": "FRIENDS_WITH"},
            "update_time": "2025-04-28T12:10:00Z",
        },
        {
            "relation_id": 102,
            "source_id": 2,
            "target_id": 3,
            "properties": {"type": "COWORKERS_WITH"},
            "update_time": "2025-04-28T12:12:00Z",
        },
    ]
    with open(
        os.path.join(base_dir, "logs", "relation_updates.jsonl"), "w", encoding="utf-8"
    ) as f:
        for record in relation_logs:
            f.write(json.dumps(record) + "\n")

    # entities/shard_0.jsonl: already compacted version
    compacted_entities = [
        {
            "entity_id": 0,
            "properties": {
                "name": "Bill",
                "type": "Person",
                "email": "bill@example.com",
            },
            "last_update_time": "2025-04-28T11:05:00Z",
        },
        {
            "entity_id": 1,
            "properties": {
                "name": "Alice",
                "type": "Person",
                "email": "alice@example.com",
                "community_id": "team_alpha",
            },
            "last_update_time": "2025-04-28T12:05:00Z",
        },
        {
            "entity_id": 2,
            "properties": {
                "name": "Bobby",
                "type": "Person",
                "community_id": "team_alpha",
            },
            "last_update_time": "2025-04-28T12:06:00Z",
        },
        {
            "entity_id": 3,
            "properties": {
                "name": "Charlie",
                "type": "Person",
                "community_id": "team_beta",
            },
            "last_update_time": "2025-04-28T12:02:00Z",
        },
    ]
    with open(
        os.path.join(base_dir, "entities", "shard_0.jsonl"), "w", encoding="utf-8"
    ) as f:
        for record in compacted_entities:
            f.write(json.dumps(record) + "\n")

    # relations/shard_0.jsonl: same as relation_logs
    with open(
        os.path.join(base_dir, "relations", "shard_0.jsonl"), "w", encoding="utf-8"
    ) as f:
        for record in relation_logs:
            f.write(json.dumps(record) + "\n")

    # adjacency/adjacency.jsonl: based on relations
    adjacency = [
        {"entity_id": 1, "relations": [101]},
        {"entity_id": 2, "relations": [102]},
    ]
    with open(
        os.path.join(base_dir, "adjacency", "adjacency.jsonl"), "w", encoding="utf-8"
    ) as f:
        for record in adjacency:
            f.write(json.dumps(record) + "\n")

    return base_dir


# Run and return path
create_test_graph_fixture()
