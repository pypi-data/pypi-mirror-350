import json
import os

from .base_indexer import BaseIndexer


class MemoryIndexer(BaseIndexer):
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.map = {}

    def add_entity(self, entity_id, properties):
        self.map[entity_id] = properties.get("name", None)

    def finalize(self):
        path = os.path.join(self.output_dir, "memory_index.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.map, f, indent=2)
