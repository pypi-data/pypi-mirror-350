from dataclasses import dataclass


@dataclass
class GraphReaderConfig:
    base_dir: str
    indexer_type: str = "memory"
    cache_size: int = 1000
