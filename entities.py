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
    def __init__(self, application, service, repo, version, dependencies, rollout_plan=None, timestamp=None):
        self.application = application
        self.service = service
        self.repo = repo
        self.version = version
        self.dependencies = dependencies
        self.rollout_plan = rollout_plan
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now().isoformat()
    
    def __repr__(self) -> str:
        return f"({self.application}, {self.service}, {self.repo}, {self.version}, {self.dependencies}, \
            {self.rollout_plan}, {self.timestamp})"

class Application:
    def __init__(self, name, timestamp=None, services = None):
        self.name = name
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now().isoformat()
        self.services = services
    
    def __repr__(self) -> str:
        return f"({self.name}, {self.timestamp}, {self.services})"
