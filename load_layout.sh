#!/bin/bash

i3-msg "workspace 1; append_layout ~/.config/i3/workspace_1.json"
# (librewolf &)
# (mpv &)
(setsid librewolf)
(setsid kitty)
