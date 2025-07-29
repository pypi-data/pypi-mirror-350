class PyppError(Exception):
    """Base class for pygame++ errors"""
    pass
class AssetNotFoundError(PyppError):
    """When an asset is not found (sound, image or smth)"""
    def __init__(self, path, message="Failed to load Unknown asset"):
        super().__init__(f"{message}: {path}")
        self.path = path