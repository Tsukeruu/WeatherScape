from dataclasses import dataclass
from .Exceptions import UnknownType

import argparse

@dataclass
class Args:
    _parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="A program that changes your hyprland/wayland setup regarding the weather",
            allow_abbrev=False
        )

    def add_args(
            self,
            shortcut: str,
            name: str, 
            required: bool,
            _type: str,
            action: str,
            group: self._parser.add_mutually_exclusive_group=None,
            _help: str = "A default arg!")-> None:

        if not group:
            if _type == "bool":
                self._parser.add_argument(
                    shortcut,
                    name,
                    help=_help,
                    required=required,
                    action=action
                )
            elif _type == "regular":
                self._parser.add_argument(
                    shortcut,
                    name,
                    help=_help,
                    required=required,
                    action=action
                )
            else:
                raise UnknownType()

        elif group:
            group.add_argument(
                shortcut,
                name,
                help=_help,
                required=required,
                action=action
              )
            
        else:
            pass
    
    def create_args(self) -> None:
         _execution: List[Callable[[], None]] = [
            lambda: self.add_args("-q","--quiet",False,"bool","store_true", _help="Enables quiet mode, no logging"),
            #We set both swww and hyprpaper to false simply because we already defined a exclusive group and set required to true there
            lambda: self.add_args("-sw", "--swww", False, "bool", "store_true", group=self._wallpaperGroup, _help="Use the swww wallpaper manager"),
            lambda: self.add_args("-hyp", "--hyprpaper", False, "bool", "store_true", group=self._wallpaperGroup, _help="Use the hyprpaper wallpaper manager")
         ]
         #Exclusive group means both are required but one is needed for it to execute
         self._wallpaperGroup: Any = self._parser.add_mutually_exclusive_group(required=True) 
         for execution in _execution:
             execution()

    def __post_init__(self):
         self.create_args()
         self._args: Any = self._parser.parse_args()

