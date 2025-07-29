import json
import os
from datetime import UTC, datetime

from .indexers import get_indexer


class GraphBuilder:
    def __init__(self, config):
        self.config = config
        os.makedirs(os.path.join(config.output_dir, "entities"), exist_ok=True)
        os.makedirs(os.path.join(config.output_dir, "relations"), exist_ok=True)
        os.makedirs(os.path.join(config.output_dir, "logs"), exist_ok=True)

        self.entity_log_path = os.path.join(
            config.output_dir, "logs", "entity_updates.jsonl"
        )
        self.relation_log_path = os.path.join(
            config.output_dir, "logs", "relation_updates.jsonl"
        )

        self.indexer = get_indexer(config.indexer_type, config.output_dir)

    def _get_now_timestamp(self):
        return datetime.now(UTC).isoformat() + "Z"

    def add_entity(self, entity_id, properties, update_time=None):
        update_time = update_time or self._get_now_timestamp()
        record = {
            "entity_id": entity_id,
            "properties": properties,
            "update_time": update_time,
        }
        with open(self.entity_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        self.indexer.add_entity(entity_id, properties)

    def add_relation(
        self, relation_id, source_id, target_id, properties, update_time=None
    ):
        update_time = update_time or self._get_now_timestamp()
        record = {
            "relation_id": relation_id,
            "source_id": source_id,
            "target_id": target_id,
            "properties": properties,
            "update_time": update_time,
        }
        with open(self.relation_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def finalize(self):
        self.indexer.finalize()
