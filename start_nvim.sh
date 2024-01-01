#!/bin/bash
nvim
echo $NVIM_LISTEN_ADDRESS > /tmp/nvim_listen_address_$(tmux display-message -p '#{pane_id}')_$(kitty @ ls | jq -r '.[0].id')

