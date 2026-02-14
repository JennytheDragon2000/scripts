
  ~/.local/bin/youtube-wifi-switcher.sh — The polling script that:
  - Checks the focused Sway window title every 3 seconds via swaymsg -t get_tree | jq
  - Case-insensitive match for "YouTube" in the title
  - Debounces with 2 consecutive checks (6 seconds) before switching
  - Skips nmcli calls if already on the correct network
  - Logs all switches to ~/.local/share/youtube-wifi-switcher/switcher.log
  - SSID config variables at the top for easy editing

  ~/.config/systemd/user/youtube-wifi-switcher.service — Systemd user service with restart-on-failure.

  To test manually first:

  bash ~/.local/bin/youtube-wifi-switcher.sh

  Open YouTube in Firefox and switch between tabs to verify it works. Check logs with:

  tail -f ~/.local/share/youtube-wifi-switcher/switcher.log

  Once confirmed, enable the service:

  systemctl --user enable --now youtube-wifi-switcher.service
