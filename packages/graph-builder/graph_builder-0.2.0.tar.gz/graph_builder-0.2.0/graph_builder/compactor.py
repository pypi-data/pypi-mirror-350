import json
import os
from collections import defaultdict


class GraphCompactor:
    def __init__(self, base_dir, shard_size=1000):
        self.base_dir = base_dir
        self.shard_size = shard_size
        os.makedirs(os.path.join(base_dir, "entities"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "adjacency"), exist_ok=True)

    def compact_entities(self):
        entity_versions = defaultdict(list)
        entity_log_path = os.path.join(self.base_dir, "logs", "entity_updates.jsonl")
        with open(entity_log_path, encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                entity_id = record["entity_id"]
                entity_versions[entity_id].append(record)

        shard_id = 0
        buffer = []
        for _entity_id, updates in entity_versions.items():
            merged = self._merge_updates(updates)
            buffer.append(merged)
            if len(buffer) >= self.shard_size:
                self._flush_entities(buffer, shard_id)
                buffer = []
                shard_id += 1
        if buffer:
            self._flush_entities(buffer, shard_id)

    def _merge_updates(self, updates):
        updates = sorted(updates, key=lambda x: x["update_time"])
        merged_properties = {}
        last_update_time = None
        for upd in updates:
            for k, v in upd["properties"].items():
                merged_properties[k] = v
            last_update_time = upd["update_time"]
        return {
            "entity_id": updates[0]["entity_id"],
            "properties": merged_properties,
            "last_update_time": last_update_time,
        }

    def _flush_entities(self, buffer, shard_id):
        path = os.path.join(self.base_dir, "entities", f"shard_{shard_id:05}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for record in buffer:
                f.write(json.dumps(record) + "\n")

    def build_adjacency(self):
        relation_log_path = os.path.join(
            self.base_dir, "logs", "relation_updates.jsonl"
        )
        adjacency = defaultdict(list)
        with open(relation_log_path, encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                source_id = record["source_id"]
                adjacency[source_id].append(record["relation_id"])

        path = os.path.join(self.base_dir, "adjacency", "adjacency.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for entity_id, relations in adjacency.items():
                f.write(
                    json.dumps({"entity_id": entity_id, "relations": relations}) + "\n"
                )

    def compact_relations(self):
        """Compact relation updates into sharded files."""
        relation_log_path = os.path.join(
            self.base_dir, "logs", "relation_updates.jsonl"
        )
        os.makedirs(os.path.join(self.base_dir, "relations"), exist_ok=True)

        # Read all relations
        relations = []
        with open(relation_log_path, encoding="utf-8") as f:
            for line in f:
                relations.append(json.loads(line))

        # Sort by relation_id and update_time to ensure consistent ordering
        relations.sort(key=lambda x: (x["relation_id"], x["update_time"]))

        # Write to shard file
        shard_path = os.path.join(self.base_dir, "relations", "shard_0.jsonl")
        with open(shard_path, "w", encoding="utf-8") as f:
            for relation in relations:
                f.write(json.dumps(relation) + "\n")
