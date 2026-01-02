"""
Dependencies to install:
    Charmbracelets log library
    golang
    pywal
    hyprshot or swww
    (Use docker for efficient management?)
"""

from typing import List, Generic, TypeVar, Dict, Any, Union
from utils.pyUtils.Exceptions import InvalidCode, InvalidStatus, ZeroWallpapers
import requests
import os
import random

T = TypeVar("T")

"""
A valid way to write the logging modes is this:
   severities include but are not limited to: Info, Error, Warn, Debug (limited options which havent been added are Fatal and more)
   run the static method (Logging) if it were a custom message, provide custommsg and severity, otherwise if its for error handling (requests) then dont bother
   ex: Logging("Custom", "This is a custom info msg", "Info")
   Some functions have a default logging message which is enabled by setting the logging arguement to true
   Those default loggers usually have a description of what is currently being done
"""

class main():
    @staticmethod
    def Logging(Status: T, CustomMsg = None, Severity = None) -> None:
        if Status == "Success" and (type(Status) == str):
            os.system(f"cd utils && go run logging.go {Status}")
        elif Status == "Fail" and (type(Status) == str):
             os.system(f"cd utils && go run logging.go {Status}")
        elif Status == "Custom" and (type(Status) == str):
             os.system(f'cd utils && go run logging.go {Status} "{CustomMsg}" {Severity}')
        else:
            raise InvalidStatus()

    def __init__(self, logging: bool = False) -> None:
        self._URL_Json: str = "https://wttr.in/?format=j1"
        self._WeatherCodes: Dict[str, Dict[int]]  = {
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
        self.currentDir = os.getcwd()
        try:
            self.Weather: List[Any] = self.makeRequest(True)
            self.Condition = self.classify(self.Weather[-1], True)
            self.Logging("Success")
            print(self.returnFiles(True))
        except requests.exceptions.ConnectionError as f:
            self.Logging("Fail")
        except InvalidStatus as g:
            self.Logging("Custom","A status was not found","Error")
            return 
        except ZeroWallpapers as e:
            self.Logging("Custom","Zero wallpapers found in chosen dir/condition, are there any wallpapers in mind?", "Warn")
        except InvalidCode as h:
            self.Logging("Custom","The weather code provided is not correct, are you even on earth?", "Error")

    def classify(self, code: int, logging = False) -> str:
        if logging == True:
            self.Logging("Custom", "Finding condition via given weather code...", "Debug")
        for condition, codes in self._WeatherCodes.items():
            if code in codes:
                return condition

        raise InvalidCode(code)

    def makeRequest(self, logging: bool = False) -> List[Any]:
        if logging == True:
            self.Logging("Custom","Attempting to do a GET request towards wttr.in!","Debug")
        data: List[Any] = []
        self.WeatherData = requests.get(self._URL_Json).json()
        self.AreaName: str = self.WeatherData["nearest_area"][0]["areaName"][0]["value"]
        self.currentWeather: str = self.WeatherData["current_condition"][0]["weatherDesc"][0]["value"]
        self.Temp_C: int = self.WeatherData["current_condition"][0]["FeelsLikeC"]
        self.Temp_F: int = self.WeatherData["current_condition"][0]["FeelsLikeF"]
        self.currentCode: int = int(self.WeatherData["current_condition"][0]["weatherCode"])
        data.extend([self.AreaName, self.currentWeather, self.Temp_C, self.Temp_F, self.currentCode])
        
        return data

    def navigation(self, currentCondition: str, logging: bool = False) -> str:
        if logging == True:
            self.Logging("Custom", "Navigating through conditions...", "Debug")
        return f"{self.currentDir}/wallpapers/{currentCondition}"

    def returnFiles(self, logging: bool = False) -> List[Union[str, None]]:
        if logging == True:
            self.Logging("Custom","Listing files in the dir!", "Debug")
        self.chosenDir: str = self.navigation(self.Condition, True)
        self.currentFiles: List[Union[str, None]] = []
        self.allFiles: str = os.listdir(self.chosenDir)
        for file in self.allFiles:
            self.currentFiles.append(file)
        if not self.currentFiles:
            raise ZeroWallpapers()
        else:
            self.Logging("Custom",f"Found ({len(self.currentFiles)})! wallpapers for {self.Condition}","Info")

        return self.currentFiles
    
    def applytheme(self, logging: bool = False) -> None:
        pass #use gum to ask them if they want to run pywal and perform changes to the colorscheme, ofcourse after we randomize the list of files in self.allfiles

X = main()
