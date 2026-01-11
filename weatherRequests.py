"""
Dependencies to install:
    Charmbracelets log library
    golang
    pywal
    swww
    #2 modes, cli mode and rofi dmenu mode if you want
"""

from typing import List, Generic, TypeVar, Dict, Any, Union, ClassVar, Set
from dataclasses import dataclass
from utils.pyUtils.Exceptions import InvalidCode, InvalidStatus, ZeroWallpapers, SwwwFailed, WalFailed
from utils.pyUtils.Dataclasses import ConfigInit
import requests
import os
import random
import subprocess
import configparser

T = TypeVar("T")

"""
A valid way to write the logging modes is this:
   severities include but are not limited to: Info, Error, Warn, Debug (limited options which havent been added are Fatal and more)
   run the static method (Logging) if it were a custom message, provide custommsg and severity, otherwise if its for error handling (requests) then dont bother
   ex: Logging("Custom", "This is a custom info msg", "Info")
   Some functions have a default logging message which is enabled by setting the logging arguement to true
   Those default loggers usually have a description of what is currently being done
"""

class main(ConfigInit):
    @staticmethod
    def Logging(Status: T, CustomMsg = None, Severity = None) -> None:
        if Status == "Success" and (isinstance(Status, str)):
            os.system(f"cd utils && go run logging.go {Status}")
        elif Status == "Fail" and (isinstance(Status, str)):
             os.system(f"cd utils && go run logging.go {Status}")
        elif Status == "Custom" and (isinstance(Status, str)):
             os.system(f'cd utils && go run logging.go {Status} "{CustomMsg}" {Severity}')
        else:
            raise InvalidStatus()

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
        return f"{self._currentDir}/wallpapers/{currentCondition}"

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
        randomizedWalPath: str = f"{self._currentDir}/wallpapers/{self.Condition}/{self.selectedWallpaper}"
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
            self.Logging("Custom","Unable to run swww! Is the daemon running?","Error")
            return
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
            self.restartBar("eww",self._Eww_Reset, True)
            self.hyprLock(self._Hyprlock_Set, True)
    #Optional, add or remove depending on your status bar and hyprlock!
    def restartBar(self, statusBar: str, execute: bool, logging: bool = False) -> None:
        if execute:
            if logging == True:
                self.Logging("Custom", "Restarting eww bar for USER", "Debug")
            else:
                pass
            os.system(f"sh utils/ShellUtil.sh Eww")
        else:
            self.Logging("Custom", "Eww reset not enabled", "Debug")

    def hyprLock(self,execute: bool, logging: bool = False) -> None:
        if execute:
            if logging == True:
                self.Logging("Custom","Changing hyprlock...","Debug")
            else:
                pass
            os.system(f'sh utils/ShellUtil.sh hyprLock {self.selectedWallpaper} {self.Condition} {self._currentDir}')
        else:
            self.Logging("Custom","Setting hyprlock is not enabled","Debug")

app = main(_init_logging=True)


#Add notify-send
#Use configparser and make an ini config file
#Make this modular by dividing up the classes into seperate files and making it cleaner
