from dataclasses import dataclass
from typing import ClassVar, Dict, Set
from utils.pyUtils.Exceptions import InvalidCode, InvalidStatus, ZeroWallpapers, SwwwFailed, WalFailed
import os

@dataclass
class ConfigInit:
    _hyprlockPath: str = "~/.config/hypr/hyprlock.conf"
    _URL_Json: str = "https://wttr.in/?format=j1"
    _swww_duration: int = 1.5
    _swww_transition: int = "fade"
    _currentDir: str = os.getcwd()
    _WeatherCodes: ClassVar[Dict[str, set[int]]] = {
        "clear": {113},
        "partly_cloudy": {116},
        "cloudy": {119, 122},
        "fog": {143, 248, 260},
        "drizzle": {263, 266},
        "rain": {176,293,296,299,302,305,308},
        "sleet": {281,284,317, 320, 362, 365},
        "snow": {179, 323, 326, 329, 332, 335, 338},
        "snow_showers": {368,371},
        "hail": {350, 374, 377},
        "thunderstorm": {200, 386, 389, 392, 395}
    }
    _init_logging: bool = False


    def __post_init__(self) -> None:
        if self._init_logging == True:
            self.Logging("Custom","Initialized variables!", "Info")
        else:
            pass
        try:
            self.Weather: List[Any] = self.makeRequest(True)
            self.Condition = self.classify(self.Weather[-1], True)
            self.Logging("Success")
            print(self.returnFiles(True))
            self.applyWal(True) 
        except requests.exceptions.ConnectionError as f:
            self.Logging("Fail")
            return
        except InvalidStatus as g:
            self.Logging("Custom","A status was not found","Error")
            return 
        except ZeroWallpapers as e:
            self.Logging("Custom","Zero wallpapers found in chosen dir/condition, are there any wallpapers in mind?", "Warn")
            return
        except InvalidCode as h:
            self.Logging("Custom","The weather code provided is not correct, are you even on earth?", "Error")
            return
        except WalFailed as j:
            self.Logging("Custom","Fail; No image found!","Error")  
            return        
