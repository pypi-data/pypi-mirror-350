#!/bin/bash
# Send command to tmux session and read output
tmux send-keys -t excel-mcp "$1" Enter && sleep 2 && tmux capture-pane -t excel-mcp -p -S -30