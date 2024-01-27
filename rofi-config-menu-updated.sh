#!/usr/bin/env bash

DMEDITOR="kitty -c /home/jenny/.config/kitty/kitty.conf -e nvim -u /home/jenny/.config/nvim/init.lua"
# DMEDITOR="kitty zsh -c 'nvim'"
PDFVIEWER="zathura"

declare -a options=(
"Alacritty - /home/jenny/.config/alacritty/alacritty.yml"
"AwesomeWM - /home/jenny/.config/awesome/rc.lua"
"Bash - /home/jenny/.bashrc"
"NeoVim - /home/jenny/.config/nvim/init.lua"
"Picom - /home/jenny/.config/picom/picom.conf"
"Rofi - /home/jenny/.config/rofi/config.rasi"
"rconfig - /home/jenny/scripts/rofi-config-menu-updated.sh"
"Ranger - /home/jenny/.config/ranger/rc.conf"
"Zsh - /home/jenny/.zshrc"
"i3 - /home/jenny/.config/i3/config"
"alias - /home/jenny/.config/aliasrc"
"lf - /home/jenny/.config/lf/lfrc"
"polybar - /home/jenny/.config/polybar/config.ini"
"qutebrowser - /home/jenny/.config/qutebrowser/config.py"
"kitty - /home/jenny/.config/kitty/kitty.conf"
"tmux - /home/jenny/.tmux.conf"
"mpv - /home/jenny/.config/mpv/mpv.conf"
"mpvInputs - /home/jenny/.config/mpv/input.conf"
"sxhkd - /home/jenny/.config/sxhkd/sxhkdrc"
"mathsCw - /home/jenny/Semester2/Maths-Cw-2022.pdf"
"keyd - /etc/keyd/default.conf"
"live-server - /home/jenny/.live-server.json"
"environmet-variables - /etc/environment"
"wget - /home/jenny/.wgetrc."
"sway - /home/jenny/.config/sway/config"
"kmonad - /home/jenny/.config/kmonad/config.kbd"
"dnf - /etc/dnf/dnf.conf"
"git - /etc/gitconfig"
"axel - /etc/axelrc"
"fish - /home/jenny/.config/fish/config.fish"
"espanso - /home/jenny/.config/espanso/match/base.yml"
"kitty - /home/jenny/.config/kitty/open-actions.conf"
"PermenentMount - /etc/fstab"
"proxychains - /etc/proxychains.conf"


"Quit"
)

choice=$(printf '%s\n' "${options[@]}" | rofi -theme /home/jenny/.config/rofi/config.rasi -dmenu -i  20 -p 'Edit config:')

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1

elif [ "$choice" ]; then
	cfg=$(printf '%s\n' "${choice}" | awk '{print $NF}')

	if [[ "$cfg" == *".pdf" ]]; then
		$PDFVIEWER "$cfg"
		exit 0
	fi

    if [[ "$cfg" == *".config/nvim"* ]]; then
		cd "/home/jenny/.config/nvim/"
	fi

	$DMEDITOR "$cfg"

else
    echo "Program terminated." && exit 1
fi

