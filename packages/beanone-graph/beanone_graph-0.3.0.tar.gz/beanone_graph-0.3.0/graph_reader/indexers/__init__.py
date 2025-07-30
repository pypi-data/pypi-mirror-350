import os


def get_indexer(indexer_type, base_dir):
    if base_dir is None:
        raise TypeError("base_dir cannot be None")
    if not base_dir:
        raise ValueError("base_dir cannot be empty")

    if indexer_type == "sqlite":
        from .sqlite_indexer import SQLiteIndexer

        return SQLiteIndexer(base_dir)
    elif indexer_type == "memory":
        from .memory_indexer import MemoryIndexer

        return MemoryIndexer(base_dir)
    else:
        raise ValueError(f"Unknown indexer type: {indexer_type}")
