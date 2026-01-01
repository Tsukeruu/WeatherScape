class InvalidCode(Exception):
    def __init__(self, code: int, message: str = None):
        if message == None:
            message = f"Invalid weather code for {code}"
        super().__init__(message)

class InvalidStatus(Exception):
    def __init__(self, message: str = None):
        if message == None: 
            message = "Unable to understand status provided!"
        super().__init__(message)

class ZeroWallpapers(Exception):
    def __init__(self, message: str = None):
        if message == None:
            message = "No wallpapers found in chosen dir/condition"
        super().__init__(message)
