hyprLock="$HOME/.config/hypr/hyprlock.conf"
hyprPaper="$HOME/.config/hypr/hyprpaper.conf"

main() {
  sed -i -e "s|path = .*|path = $currentDir/wallpapers/$condition/$chosenImage|" $hyprLock
}

if [[ $1 = "Eww" ]]; then
 eww kill && eww open-many bar notifications >/dev/null 2>&1
fi

if [[ $1 = "hyprLock" ]]; then
  chosenImage=$2
  condition=$3
  currentDir=$4
  main
fi

if [[ $1 = "hyprSnow-enable" ]]; then
  if pgrep -x hyprsnow; then
    pkill hyprsnow && hyprsnow &
  else
    hyprsnow &
  fi
fi

if [[ $1 = "hyprSnow-disable" ]]; then
  if pgrep -x hyprsnow; then
    pkill hyprsnow
  else 
    pkill hyprsnow
  fi
fi

if [[ $1 = "hyprpaper" ]]; then
  chosenImage=$2
  condition=$3
  currentDir=$4
  sed -i -e "s|preload = .*|preload = $currentDir/wallpapers/$condition/$chosenImage|" $hyprPaper
  sed -i -e "s|path = .*|path = $currentDir/wallpapers/$condition/$chosenImage|" $hyprPaper
  pkill hyprpaper && hyprpaper &
fi
