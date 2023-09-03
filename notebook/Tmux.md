# Tmux

## From the shell
To start a new session
```
tmux
tmux new -s <name>
```
To attach to a session
```
tmux attach
tmux attach -t <name>
```
To list session
```
tmux ls
```
To kill a session
```  
tmux kill-session -t <name>
```

## Within tmux
The command after hitting the prifix key `Ctrl-B`

### Session
| Command | Function |
|---------|----------|
|:new<CR>|Start a new session|
|s|List sessions|
|$|Rename a session|
|(|Go to previous session|
|)|Go to next session|

### Window
| Command | Function |
|---------|----------|
|c|Create a new window|
|,|Rename a window|
|w|List windows|
|f|Find a window|
|&|Kill a window|
|p|Go to previous window|
|n|Go to next window|
|:swap-window -s 2 -t 1|Swap 2 and 1|
|:swap-window -t -1|Move the current windows to the left by 1 position|
|.|Move window - prompted for a new number|
|:movew<CR>|Move window to the next unused number|

### Pane
| Command | Function |
|---------|----------|
|%|Horizontal split|
|"|Vertical split|
|o|Switch panes|
|q|Show pane numbers|
|q `num`|Go to the pane number|
|x|Kill a pane|
|z|Zoom|
|!|Convert pane into window|
|space|Toggle between layouts|
|{|Move the current pane left|
|}|Move the current pane right|

### Tmux plugin manager
| Command | Function |
|---------|----------|
|I|Install|
|U|Update|

### tmux-resurrect
| Command | Function |
|---------|----------|
|Ctrl-s|Save the session|
|Ctrl-r|Restore the previous session|

### Miscellenous
| Command | Function |
|---------|----------|
|d|Detach from the current session|
|t|Show a big clock|
|?|List shortcuts|
|:|Go to prompt|
|`Ctrl-x`|(while holding `Ctrl`) Toggle synchronize-panes|

## From Tmux Command Prompt
Toggle or turn on/off pane synchronization
```
:setw synchronize-panes
:setw synchronize-panes on
:setw synchronize-panes off
```

Reference
- https://tmuxcheatsheet.com/
- https://www.sitepoint.com/10-killer-tmux-tips/
