class Cache:
    def __init__(self):
        self.map = {}
    
    def set(self, key, value):
        self.map[key] = value
        return True
    
    def get(self, key):
        return self.map[key]
    
    def get_size(self):
        return len(self.map)