#!/bin/bash


cat << "EOF"
WEATHERSCAPE INSTALLATION; VERSION (1.0.0)

                _                                  
              (`  ).                   _           
             (     ).              .:(`  )`.       
)           _(       '`.          :(   .    )      
        .=(`(      .   )     .--  `.  (    ) )      
       ((    (..__.:'-'   .+(   )   ` _`  ) )                 
`.     `(       ) )       (   .  )     (   )  ._   
  )      ` __.:'   )     (   (   ))     `-'.-(`  ) 
)  )  ( )       --'       `- __.'         :(      )) 
.-'  (_.'          .')                    `(    )  ))
                  (_  )                     ` __.:'          
                                        
--..,___.--,--'`,---..-.--+--.,,-,,..._.--..-._.-a:f--.
EOF

ubuntu() {
   sudo apt update
   sudo apt install python3-pip imagemagick
   sudo pip3 install pywal
   sudo apt install build-essential pkg-config liblz4-dev git
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source $HOME/.cargo/env
   git clone https://github.com/LGFae/swww.git
   cd swww
   cargo build --release
   sudo cp target/release/swww target/release/swww-daemon /usr/local/bin/
   sudo add-apt-repository ppa:longsleep/golang-backports && sudo apt update && sudo apt install golang-go
}

Installation() {
 if [[ $1 = "arch" ]]; then
  sudo pacman -S python-pywal
  sudo pacman -S swww
  sudo pacman -S go
 elif [[ $1 = "fedora" ]]; then
   sudo dnf copr enable luisbocanegra/kde-material-you-colors
   sudo dnf copr enable materka/swww
   sudo dnf install python-pywal
   sudo dnf install swww
   sudo dnf install golang
 elif [[ $1 = "ubuntu" ]]; then
   ubuntu
 fi
}

if command -v "pacman"; then
  echo "Arch/Endeavour setup detected..."
  read -p "Would you like to install the dependencies? (Y/N): " installDependencies
  if [[ "$installDependencies" = "Y" || "$installDependencies" = "y" ]]; then
    Installation "arch" 
  else
    exit
  fi
elif command -v "dnf"; then
  echo "Red hat setup detected..."
  read -p "Would you like to install the dependencies? (Y/N): " installDependencies
  if [[ "$installDependencies" = "Y" || "$installDependencies" = "y" ]]; then
    Installation "fedora"
  else 
    exit
  fi
elif command -v "apt"; then
  echo "Ubuntu/Pop setup detected..."
  read -p "Would you like to install the dependencies (Y/N): " installDependencies
  if [[ "$installDependencies" = "Y" || "$installDependencies" = "y" ]]; then
    Installation "ubuntu"
  else 
    exit
  fi
else 
  echo "Distro not detected, please check how to install the dependencies from your package manager"
fi
