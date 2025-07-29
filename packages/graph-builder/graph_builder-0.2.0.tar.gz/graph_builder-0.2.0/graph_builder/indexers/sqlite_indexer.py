import os
import sqlite3

from .base_indexer import BaseIndexer


class SQLiteIndexer(BaseIndexer):
    def __init__(self, output_dir):
        self.db_path = os.path.join(output_dir, "index.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entity_index (
                entity_id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        self.conn.commit()

    def add_entity(self, entity_id, properties):
        name = properties.get("name", None)
        self.cursor.execute(
            "INSERT OR REPLACE INTO entity_index (entity_id, name) VALUES (?, ?)",
            (entity_id, name),
        )

    def finalize(self):
        self.conn.commit()
        self.conn.close()
