from dataclasses import dataclass
import argparse

@dataclass
class Args:
    _parser = argparse.ArgumentParser(
            description="A program that changes your hyprland/wayland setup regarding the weather",
            allow_abbrev=False
        )

    def __post_init__(self): 
         self._parser.add_argument(
            "-q", 
            "--quiet",
            help="Enables quiet mode, no logging", 
            required=False, #doesnt require on startup
            action="store_true" #store_true means its false if not specified
        )
         self._args = self._parser.parse_args()

