#!/usr/bin/env bash
#
# A script to call cheat sheet to query how to use e.g. unix commands
# We store the list of favorite languages and commands to query in
# separate files. This is because cht.sh operates differently between
# the two groups.
#
# From https://www.youtube.com/watch?v=hJzqEAf2U4I

config=$HOME/Workspace/scripts/config
languages=$config/tmux_cht_languages
commands=$config/tmux_cht_commands
# Use fuzzy finder so that we don't have to type the whole word
selected=`cat $languages $commands | fzf`
if [[ -z $selected ]]; then
	exit 0
fi

read -p "Enter Query: " query

if grep -qs "$selected" $languages; then
   query=`echo $query | tr ' ' '+'`
   tmux neww bash -c "echo \"curl cht.sh/$selected/$query/\" & curl cht.sh/$selected/$query & while [ : ]; do sleep 1; done"
else
	# tmux neww will create a window to run the command and
   # close the window immediately after the command terminate.
   tmux neww bash -c "curl -s cht.sh/$selected~$query | bat"
fi
