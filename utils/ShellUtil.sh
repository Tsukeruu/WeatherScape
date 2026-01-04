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
