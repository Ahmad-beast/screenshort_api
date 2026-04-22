import time

class CacheManager:
    def __init__(self, expiration_time=300): # 5 minutes default expiration
        self.cache = {}
        self.expiration_time = expiration_time

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.expiration_time:
                return data
            else:
                del self.cache[key] # Remove expired cache
        return None

    def set(self, key, data):
        self.cache[key] = (data, time.time())

# Global instance
screenshot_cache = CacheManager()
