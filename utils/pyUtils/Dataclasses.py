from dataclasses import dataclass
from typing import ClassVar, Dict, Set, List, Callable
from utils.pyUtils.Exceptions import InvalidCode, InvalidStatus, ZeroWallpapers, SwwwFailed, WalFailed
from pathlib import Path
from .Args import Args
import configparser
import os
import requests
import argparse


@dataclass
class ConfigInit(Args):
    _hyprlockPath: str = "~/.config/hypr/hyprlock.conf"
    _URL_Json: str = "https://wttr.in/?format=j1&num_of_days=1"
    _swww_duration: int = 1.5
    _swww_transition: int = "fade"
    _currentDir: str = Path(__file__).parent.parent.parent
    _configDir: str = Path.home() / ".config" / "weatherscape"
    _configFile: str =  Path.home() / ".config" / "weatherscape" / "MyConfig.ini"
    _configParser = configparser.ConfigParser() 
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

    @staticmethod
    def WriteToFile(filePath: str, Content: str = None) -> None:
        if Content == None:
            Content = Path(__file__).parent.parent / "pyUtils" / "Text_Files" / "Default_Config.txt" #Path(__file__) returns where the file is located regardless of where i am, .parent returns the parent dir
            Content = Content.read_text()
        else:
            pass
        filePath.write_text(Content, encoding='utf-8')

    def ReturnConfigValues(self, configFile: str, keys: List[str], Title: str) -> List[bool]:
        self._configParser.read(configFile)
        returnedValues: List[bool] = []
        for key in keys:
            result = self._configParser.getboolean(Title, key) #consider adding generics and using isinstance or type() for each configparser field
            returnedValues.append(result)

        return returnedValues
            
    def __post_init__(self) -> None: 
        super().__post_init__() #We called this because our init and post_init overrides Args.py's post_init and init, so they never exist, we did this because we call parent class's post init and init to initialize args, so then it can be passed down properly
        if self._init_logging == True:
            self.Logging(
                "Custom",
                "Initialized variables!",
                "Info"
            )
        else:
            pass
        
        if self._configDir.is_dir() and self._configFile.is_file():
            self.Logging(
                "Custom",
                "Config dir and file were found!", 
                "Info"
            )
        else:
            self.Logging(
                "Custom",
                "Config dir and file were not found!",
                "Warn"
            )
            self.Logging(
                "Custom",
                "Creating..",
                "Debug"
            )
            self._configDir.mkdir(parents=True, exist_ok=True)
            self._configFile.touch(exist_ok=True)
            self.Logging(
                "Custom",
                "Forming base config file...", 
                "Debug"
            )
            self.WriteToFile(self._configFile)

        #Calling it here because either way the configfile WILL still exist
        self._Eww_Reset, self._Hyprlock_Set = self.ReturnConfigValues(self._configFile, ["Eww_Bar_Restart", "Hyprlock_Set"], "General")
        try:
            self.Weather: List[Any] = self.makeRequest(True)
            self.Condition = self.classify(self.Weather[-1], True)
            self.Logging("Success")
            self.returnFiles(True)
            self.applyWal(True) 
        except requests.exceptions.ConnectionError as f:
            self.Logging("Fail")
            return
        except InvalidStatus as g:
            self.Logging(
                "Custom",
                "A status was not found",
                "Error"
            )
            return 
        except ZeroWallpapers as e:
            self.Logging(
                "Custom",
                "Zero wallpapers found in chosen dir/condition, are there any wallpapers in mind?", 
                "Warn"
            )
            return
        except InvalidCode as h:
            self.Logging(
                "Custom",
                "The weather code provided is not correct, are you even on earth?",
                "Error"
            )
            return
        except WalFailed as j:
            self.Logging(
                "Custom",
                "Fail; No image found!",
                "Error"
            )  
            return
