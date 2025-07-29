from dataclasses import dataclass


@dataclass
class GraphBuilderConfig:
    output_dir: str
    shard_size: int = 1000  # Number of records per shard
    indexer_type: str = "sqlite"  # Options: "sqlite", "memory"
