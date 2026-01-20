class InvalidCode(Exception):
    def __init__(self, code: int, message: str = None) -> None:
        if not message:
            message = f"Invalid weather code for {code}"
        super().__init__(message)

class InvalidStatus(Exception):
    def __init__(self, message: str = None) -> None:
        if not message: 
            message = "Unable to understand status provided!"
        super().__init__(message)

class ZeroWallpapers(Exception):
    def __init__(self, message: str = None) -> None:
        if not message:
            message = "No wallpapers found in chosen dir/condition"
        super().__init__(message)

class WalFailed(Exception):
    def __init__(self, message: str = None) -> None:
        if not message:
            message = "Pywal failed to execute"

        super().__init__(message)

class SwwwFailed(Exception):
    def __init__(self, message: str = None) -> None:
        if not message:
            message = "Swww failed to set the wallpaper!"

        super().__init__(message)


class InternalError(Exception):
    def __init__(self, message: str = None) -> None:
        if not message:
            message = "An internal error occured in wttr.in.. dont worry this isnt your problem :)"

        super().__init__(message)
