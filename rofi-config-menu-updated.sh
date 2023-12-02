#!/usr/bin/env bash

DMEDITOR="kitty -c /home/srinath/.config/kitty/kitty.conf -e nvim -u /home/srinath/.config/nvim/init.lua"
# DMEDITOR="kitty zsh -c 'nvim'"
PDFVIEWER="zathura"

declare -a options=(
"Alacritty - /home/srinath/.config/alacritty/alacritty.yml"
"AwesomeWM - /home/srinath/.config/awesome/rc.lua"
"Bash - /home/srinath/.bashrc"
"NeoVim - /home/srinath/.config/nvim/init.lua"
"Picom - /home/srinath/.config/picom/picom.conf"
"Rofi - /home/srinath/.config/rofi/config.rasi"
"rconfig - /home/srinath/scripts/rofi-config-menu-updated.sh"
"Ranger - /home/srinath/.config/ranger/rc.conf"
"Zsh - /home/srinath/.zshrc"
"i3 - /home/srinath/.config/i3/config"
"alias - /home/srinath/.config/aliasrc"
"lf - /home/srinath/.config/lf/lfrc"
"polybar - /home/srinath/.config/polybar/config.ini"
"qutebrowser - /home/srinath/.config/qutebrowser/config.py"
"kitty - /home/srinath/.config/kitty/kitty.conf"
"tmux - /home/srinath/.tmux.conf"
"mpv - /home/srinath/.config/mpv/mpv.conf"
"mpvInputs - /home/srinath/.config/mpv/input.conf"
"sxhkd - /home/srinath/.config/sxhkd/sxhkdrc"
"mathsCw - /home/srinath/Semester2/Maths-Cw-2022.pdf"
"keyd - /etc/keyd/default.conf"
"live-server - /home/srinath/.live-server.json"
"environmet-variables - /etc/environment"
"wget - /home/srinath/.wgetrc."
"sway - /home/srinath/.config/sway/config"
"kmonad - /home/srinath/.config/kmonad/config.kbd"
"dnf - /etc/dnf/dnf.conf"
"git - /etc/gitconfig"
"axel - /etc/axelrc"
"fish - /home/srinath/.config/fish/config.fish"
"espanso - /home/srinath/.config/espanso/match/base.yml"


"Quit"
)

choice=$(printf '%s\n' "${options[@]}" | rofi -theme /home/srinath/.config/rofi/config.rasi -dmenu -i  20 -p 'Edit config:')

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1

elif [ "$choice" ]; then
	cfg=$(printf '%s\n' "${choice}" | awk '{print $NF}')

	if [[ "$cfg" == *".pdf" ]]; then
		$PDFVIEWER "$cfg"
		exit 0
	fi

    if [[ "$cfg" == *".config/nvim"* ]]; then
		cd "/home/srinath/.config/nvim/"
	fi

	$DMEDITOR "$cfg"

else
    echo "Program terminated." && exit 1
fi

