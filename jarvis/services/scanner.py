class IndexScanner:
    def __init__(self, roots, index_path, exclude, flush_interval=30, logger=None):
        ...

    def start(self):
        """Start background thread"""
    def stop(self):
        """Request stop and join short timeout"""
    def is_running(self) -> bool:
        ...
