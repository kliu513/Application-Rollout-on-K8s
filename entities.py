import datetime

class Cluster:
    def __init__(self, name, ring, config_filename):
        self.name = name
        self.ring = ring
        self.file = config_filename
        self.timestamp = datetime.datetime.now().isoformat()
    
    def __repr__(self) -> str:
        return f"({self.name}, {self.ring}, {self.file}, {self.timestamp})"