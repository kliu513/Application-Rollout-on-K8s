import datetime

class Cluster:
    def __init__(self, name, ring, config_filename, timestamp=None):
        self.name = name
        self.ring = ring
        self.config = config_filename
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now().isoformat()
    
    def __repr__(self) -> str:
        return f"({self.name}, {self.ring}, {self.config}, {self.timestamp})"

class Service:
    def __init__(self, name, repo, dependencies, timestamp=None):
        self.name = name
        self.repo = repo
        self.dependencies = dependencies if isinstance(dependencies, list) else dependencies.split(" ")
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now().isoformat()
    
    def __repr__(self) -> str:
        return f"({self.name}, {self.repo}, {self.dependencies}, {self.timestamp})"
