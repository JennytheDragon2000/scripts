#!/usr/bin/env bash

# DMEDITOR="alacritty -e nvim"
DMEDITOR="kitty -e nvim"
HOME="/home/jenny"

declare -a options=(
"Alacritty - $HOME/.config/alacritty/alacritty.yml"
"AwesomeWM - $HOME/.config/awesome/rc.lua"
"Bash - $HOME/.bashrc"
"NeoVim - $HOME/.config/nvim/init.lua"
"Picom - $HOME/.config/picom/picom.conf"
"Rofi - $HOME/.config/rofi/config.rasi"
"rconfig - /opt/scripts/rofi-config-menu.sh"
"Ranger - $HOME/.config/ranger/rc.conf"
"Zsh - $HOME/.zshrc"
"i3 - $HOME/.config/i3/config"
"alias - $HOME/.config/aliasrc"
"lf - $HOME/.config/lf/lfrc"
"polybar - $HOME/.config/polybar/config.ini"
"qutebrowser - $HOME/.config/qutebrowser/config.py"
"kitty - $HOME/.config/kitty/kitty.conf"
"tmux - $HOME/.tmux.conf"
"mpvInputs - $HOME/.config/mpv/input.conf"
"mpv - $HOME/.config/mpv/mpv.conf"
"sxhkd - $HOME/.config/sxhkd/sxhkdrc"
"enviroment - /etc/environment"


"Quit"
)

choice=$(printf '%s\n' "${options[@]}" | rofi -dmenu -i  20 -p 'Edit config:')

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1

elif [ "$choice" ]; then
	cfg=$(printf '%s\n' "${choice}" | awk '{print $NF}')

    if [[ "$cfg" == *".config/nvim"* ]]; then
		cd "$HOME/.config/nvim/"
	fi

	$DMEDITOR "$cfg"

else
    echo "Program terminated." && exit 1
fi


