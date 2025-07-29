def get_indexer(indexer_type, output_dir):
    if indexer_type == "sqlite":
        from .sqlite_indexer import SQLiteIndexer

        return SQLiteIndexer(output_dir)
    elif indexer_type == "memory":
        from .memory_indexer import MemoryIndexer

        return MemoryIndexer(output_dir)
    else:
        raise ValueError(f"Unknown indexer type: {indexer_type}")
