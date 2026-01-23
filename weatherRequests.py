#!/usr/bin/python

"""
Dependencies to install:
    Charmbracelets log library
    golang
    pywal
    add rich for logging
    maybe urwid if we were to make a tui dashboard)
    swww
    #2 modes, cli mode and rofi dmenu mode if you want
"""

from typing import List, Generic, TypeVar, Dict, Any, Union, ClassVar, Set
from dataclasses import dataclass
from utils.pyUtils.Exceptions import InvalidCode, InvalidStatus, ZeroWallpapers, SwwwFailed, WalFailed, InternalError
from utils.pyUtils.Dataclasses import ConfigInit
import requests
import os
import random
import subprocess
import configparser
import sys

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
    def Logging(self, Status: T, CustomMsg: str = None, Severity: str = None) -> None:
        if not self._args.quiet:
            if Status == "Success" and (isinstance(Status, str)):
                subprocess.run(
                    f"cd utils && go run logging.go {Status}",
                    shell=True,
                    cwd=self._currentDir
                )
            elif Status == "Fail" and (isinstance(Status, str)):
                subprocess.run(
                    f"cd utils && go run logging.go {Status}",
                    shell=True,
                    cwd=self._currentDir
                )
            elif Status == "Custom" and (isinstance(Status, str)):
                subprocess.run(
                    f'cd utils && go run logging.go {Status} "{CustomMsg}" {Severity}',
                    shell=True,
                    cwd=self._currentDir
                )
            else:
                raise InvalidStatus()
        else:
            pass
    
    def classify(self, code: int, logging = False) -> str:
        if logging == True:
            self.Logging(
                    "Custom", 
                    "Finding condition via given weather code...", 
                    "Debug"
                )
        else:
            pass
        for condition, codes in self._WeatherCodes.items():
            if code in codes:
                return condition

        raise InvalidCode(code)

    def makeRequest(self, logging: bool = False) -> List[Any]:
        if logging == True:
            self.Logging(
                    "Custom",
                    "Attempting to do a GET request towards wttr.in!",
                    "Debug"
                )
        else:
            pass
        data: List[Union[str, int]] = []
        self._WeatherData: dict[str, Any] = requests.get(self._URL_Json).json()
        #Consider using typeddicts as this can get messy
        self._current_condition: List[dict[str, Union[str, List[dict[str, str]]]]] = self._WeatherData.get("current_condition")
        self._nearest_area: List[dict[str, Union[str, List[dict[str, str]]]]] = self._WeatherData.get("nearest_area")
        #Using .get ensures we dont get an error when the key doesnt exist, usually the key doesnt exist because of an error in wttr.in backend
        if (not self._current_condition) or (not self._nearest_area):
            raise InternalError()
        else:
            self.AreaName: str = self._nearest_area[0]["areaName"][0]["value"]
            self.currentWeather: str = self._current_condition[0]["weatherDesc"][0]["value"]
            self.Temp_C: int = self._current_condition[0]["FeelsLikeC"]
            self.Temp_F: int = self._current_condition[0]["FeelsLikeF"]
            self.currentCode: int = int(self._current_condition[0]["weatherCode"])
            data.extend([self.AreaName, self.currentWeather, self.Temp_C, self.Temp_F, self.currentCode])
        
        return data

    def navigation(self, currentCondition: str, logging: bool = False) -> str:
        if logging == True:
            self.Logging(
                "Custom", 
                "Navigating through conditions...", 
                "Debug"
            )
        else:
            pass
               
        return f"{self._currentDir}/wallpapers/{currentCondition}"

    def returnFiles(self, logging: bool = False) -> List[Union[str, None]]:
        if logging == True:
            self.Logging(
                    "Custom",
                    "Listing files in the dir!",
                    "Debug"
                )
        else:
            pass

        self.chosenDir: str = self.navigation(self.Condition, True) 
        self.allFiles: str = os.listdir(self.chosenDir)
        self.currentFiles: List[Union[str, None]] = [file for file in self.allFiles]
        if not self.currentFiles:
            raise ZeroWallpapers()
        else:
            self.Logging(
                    "Custom",
                    f"Found ({len(self.currentFiles)})! wallpapers for {self.Condition}",
                    "Info"
                )

        return self.currentFiles
   
    def returnRandomWallpaper(self, logging: bool = False) -> str:
        if logging == True:
            self.Logging(
                    "Custom",
                    "Returning a random wallpaper...",
                    "Debug"
                )
        else:
            pass
        self.Randomizedwallpaper: str = random.choice(self.currentFiles)
        return self.Randomizedwallpaper

    def setWallpaper(self, logging: bool = False, wallpapermnger: str = "swww") -> str: 
        if logging == True:
            self.Logging(
                    "Custom",
                    f"Using {wallpapermnger} to set the wallpaper...", 
                    "Debug"
                )
        else:
            pass
        self.selectedWallpaper: str = self.returnRandomWallpaper(True)
        randomizedWalPath: str = f"{self._currentDir}/wallpapers/{self.Condition}/{self.selectedWallpaper}"

        self.SwwwExitCode: int = subprocess.run(
                f"{wallpapermnger} img {randomizedWalPath} --transition-type {self._swww_transition} --transition-duration {self._swww_duration}",
                shell=True
            ).returncode

        if self.SwwwExitCode != 0:
            raise SwwwFailed() 
        else:
            pass
        return randomizedWalPath

    def applyWal(self, logging: bool = False) -> None:
        if logging == True:
            self.Logging(
                    "Custom",
                    "Applying colorscheme...",
                    "Debug"
                )
        else:
            pass
        
        #The callable arguements is an empty list because a callable cares about what LAMBDA passes as an arguement not what arguements the function that lambda calls no arguements are represented by an empty list, putting none is considered bad practice
        _steps: List[Callabe[[], None]] = [
            lambda: self.restartBar("Eww",self._Eww_Reset, True),
            lambda: self.hyprLock(self._Hyprlock_Set, True),
            lambda: self.notifysend(self._Notify_send,"Changed to weather", f"Applied theme according to the weather:\n{self.Condition}", True),
            lambda: self.hyprSnow(self._hyprSnow, self.detectSnow(self.Condition)),
        ]

        try:
            randomizedWalPath_: str = self.setWallpaper(True) 
        except SwwwFailed as g:
            self.Logging(
                    "Custom",
                    "Unable to run swww! Is the daemon running?",
                    "Error"
                )

            return
        result: int
        if self._args.quiet:
            result: int = subprocess.run(
                    f"wal -i {randomizedWalPath_} -e -q",
                    shell=True
                )
        else:
            result: int = subprocess.run(
                    f"wal -i {randomizedWalPath_} -e",
                    shell=True
                )

        self.WalExitCode: int = result.returncode
        if self.WalExitCode != 0:
            raise WalFailed()
        else:
            for execution in _steps:
                execution()
            """
            self.restartBar("Eww",self._Eww_Reset, True)
            self.hyprLock(self._Hyprlock_Set, True)
            self.notifysend(self._Notify_send,"Changed to weather", f"Applied theme according to the weather:\n {self.Condition}", True)
            self.hyprSnow(self._hyprSnow, self.detectSnow(self.Condition))
            """

    def restartBar(self, statusBar: str, execute: bool, logging: bool = False) -> None:
        if execute:
            if logging == True:
                self.Logging(
                        "Custom",
                        "Restarting eww bar for USER",
                        "Debug"
                    )
            else:
                pass
            subprocess.run(
                f"sh {self._currentDir}/utils/ShellUtil.sh {statusBar}",
                shell=True
            )
        else:
            self.Logging(
                "Custom",
                "Eww reset not enabled",
                "Debug"
            )

    def hyprLock(self,execute: bool, logging: bool = False) -> None:
        if execute:
            if logging == True:
                self.Logging(
                    "Custom",
                    "Changing hyprlock...",
                    "Debug"
                )
            else:
                pass
            subprocess.run(
                f"sh {self._currentDir}/utils/ShellUtil.sh hyprLock {self.selectedWallpaper} {self.Condition} {self._currentDir}",
                shell=True
            )
        else:
            self.Logging(
                "Custom",
                "Setting hyprlock is not enabled",
                "Debug"
            )

    def notifysend(self, execute: bool, title: str, body: str, logging: bool = False) -> None:
        if execute:
            if logging == True:
                self.Logging(
                    "Custom",
                    "Sending notification via the notification daemon",
                    "Info"
                )
            else:
                pass

            subprocess.run(
                f"notify-send '{title}' '{body}'",
                shell=True
            )
        else:
            self.Logging(
                "Custom",
                "Notification sending is not enabled",
                "Info"
            )

    def detectSnow(self, condition: str) -> bool:
        if (condition in self._WeatherCodes) and (condition in self._hyprSnowConditions):
            return True
        else:
            return False

    def hyprSnow(self, execute: bool, snowCondition: bool, logging: bool = False) -> None:
        if logging:
            self.Logging(
                "Custom",
                "Detecting hyprsnow..",
                "Info"
            )
        else:
            pass

        if execute and snowCondition:
            subprocess.run(
                f"sh {self._currentDir}/utils/ShellUtil.sh hyprSnow-enable",
                shell=True
            )
        else:
            subprocess.run(
                f"sh {self._currentDir}/utils/ShellUtil.sh hyprSnow-disable",
                shell=True
            )
            self.Logging(
                "Custom",
                "Hyprsnow is disabled or its not snowing",
                "Info"
            )

app = main()
