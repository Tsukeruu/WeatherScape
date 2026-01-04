hyprLock="$HOME/.config/hypr/hyprlock.conf"
chosenImage=$1
condition=$2
currentDir=$3

main() {
  sed -i -e "s|path = .*|path = $currentDir/wallpapers/$condition/$chosenImage|" $hyprLock
}

main
