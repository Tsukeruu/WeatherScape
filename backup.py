"""
Dependencies to install:
    Charmbracelets log library
    golang
    pywal
    swww
    #2 modes, cli mode and rofi dmenu mode if you want
    (Use docker for efficient management?)
"""

from typing import List, Generic, TypeVar, Dict, Any, Union
from utils.pyUtils.Exceptions import InvalidCode, InvalidStatus, ZeroWallpapers, SwwwFailed, WalFailed
import requests
import os
import random
import subprocess

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
        self._swww_duration: int = 1.5
        self._hyprlockPath: str = "~/.config/hypr/hyprlock.conf"
        self._swww_transition: str = "fade"
        self._WeatherCodes: Dict[str, Dict[int]] = {
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
            self.applyWal(True) 
        except requests.exceptions.ConnectionError as f:
            self.Logging("Fail")
        except InvalidStatus as g:
            self.Logging("Custom","A status was not found","Error")
            return 
        except ZeroWallpapers as e:
            self.Logging("Custom","Zero wallpapers found in chosen dir/condition, are there any wallpapers in mind?", "Warn")
        except InvalidCode as h:
            self.Logging("Custom","The weather code provided is not correct, are you even on earth?", "Error")
        except WalFailed as j:
            self.Logging("Custom","Fail; No image found!","Error")  

    def classify(self, code: int, logging = False) -> str:
        if logging == True:
            self.Logging("Custom", "Finding condition via given weather code...", "Debug")
        else:
            pass
        for condition, codes in self._WeatherCodes.items():
            if code in codes:
                return condition

        raise InvalidCode(code)

    def makeRequest(self, logging: bool = False) -> List[Any]:
        if logging == True:
            self.Logging("Custom","Attempting to do a GET request towards wttr.in!","Debug")
        else:
            pass
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
        else:
            pass
        return f"{self.currentDir}/wallpapers/{currentCondition}"

    def returnFiles(self, logging: bool = False) -> List[Union[str, None]]:
        if logging == True:
            self.Logging("Custom","Listing files in the dir!", "Debug")
        else:
            pass
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
   
    def returnRandomWallpaper(self, logging: bool = False) -> str:
        if logging == True:
            self.Logging("Custom","Returning a random wallpaper...","Debug")
        else:
            pass
        self.Randomizedwallpaper: str = random.choice(self.currentFiles)
        return self.Randomizedwallpaper

    def setWallpaper(self, logging: bool = False, wallpapermnger: str = "swww") -> str: 
        if logging == True:
            self.Logging("Custom",f"Using {wallpapermnger} to set the wallpaper...", "Debug")
        else:
            pass
        self.selectedWallpaper: str = self.returnRandomWallpaper(True)
        randomizedWalPath: str = f"{self.currentDir}/wallpapers/{self.Condition}/{self.selectedWallpaper}"
        self.SwwwExitCode: int = os.system(f"{wallpapermnger} img wallpapers/{self.Condition}/{self.selectedWallpaper} --transition-type {self._swww_transition} --transition-duration {self._swww_duration}")
        if self.SwwwExitCode != 0:
            raise SwwwFailed() 
        else:
            pass
        return randomizedWalPath

    def applyWal(self, logging: bool = False) -> None:
        try:
            randomizedWalPath_: str = self.setWallpaper(True) 
        except SwwwFailed as g:
            self.Logging("Custom","Unable to run swww!","Error")

        if logging == True:
            self.Logging("Custom","Applying colorscheme...","Debug")
        else:
            pass
        result: int = subprocess.run(["wal","-i",randomizedWalPath_,"-e"]) #the -e flag is important here because it stops from pausing the script
        #self.WalExitCode: int = os.system(f"wal -i {randomizedWalPath_}") Using os is deprecated
        self.WalExitCode: int = result.returncode
        if self.WalExitCode != 0:
            raise WalFailed()
        else:
            self.restartBar("eww", True)
            self.hyprLock(True)


    #Optional, add or remove depending on your status bar and hyprlock!
    def restartBar(self, statusBar: str, logging: bool = False) -> None:
        if logging == True:
            self.Logging("Custom", "Restarting eww bar for USER", "Debug")
        else:
            pass
        os.system(f"sh utils/ShellUtil.sh Eww")

    def hyprLock(self, logging: bool = False) -> None:
        if logging == True:
            self.Logging("Custom","Changing hyprlock...","Debug")
        else:
            pass
        os.system(f'sh utils/ShellUtil.sh hyprLock {self.selectedWallpaper} {self.Condition} {self.currentDir}')


X = main()

#Add changes to hyprlock and restart eww bar
#Add custom errors for sww and pywal
#Add notify-send
#In the future (tomorrow or late today) look at ways to improve and modulize it


hyprLock="$HOME/.config/hypr/hyprlock.conf"

main() {
  sed -i -e "s|path = .*|path = $currentDir/wallpapers/$condition/$chosenImage|" $hyprLock
}

if [[ $1 = "Eww" ]]; then
 killall eww && eww open-many bar notifications
fi

if [[ $1 = "hyprLock" ]]; then
  chosenImage=$2
  condition=$3
  currentDir=$4
  main
fi 

class InvalidCode(Exception):
    def __init__(self, code: int, message: str = None) -> None:
        if message == None:
            message = f"Invalid weather code for {code}"
        super().__init__(message)

class InvalidStatus(Exception):
    def __init__(self, message: str = None) -> None:
        if message == None: 
            message = "Unable to understand status provided!"
        super().__init__(message)

class ZeroWallpapers(Exception):
    def __init__(self, message: str = None) -> None:
        if message == None:
            message = "No wallpapers found in chosen dir/condition"
        super().__init__(message)

class WalFailed(Exception):
    def __init__(self, message: str = None) -> None:
        if message == None:
            message = "Pywal failed to execute"

        super().__init__(message)

class SwwwFailed(Exception):
    def __init__(self, message: str = None) -> None:
        if message == None:
            message = "Swww failed to set the wallpaper!"

        super().__init__(message)
