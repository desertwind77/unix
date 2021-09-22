# We need this guard; otherwise, scp will fail.
if status is-interactive
    #---------------------- Function ---------------------
	function mkcd -d "Create a directory and set CWD"
      command mkdir $argv
      if test $status = 0
         switch $argv[ ( count $argv ) ]
            case '-*'
            case '*'
               cd $argv[ ( count $argv ) ]
               return
         end
      end
   end  # funciton

   function notify -d "Beep when the last background job finish"
      set -l job ( jobs -l -g )
      # Disabling the following line; otherwise, this function will not work
      #or begin; echo "There are no jobs" >&2; return 1; end

      function _notify_job_$job --on-job-exit $job --inherit-variable job
         # beep
         echo -n \a
         functions -e _notify_job_$job
      end
   end # function

   function batdiff -d "Running git diff and display using bat"
      git diff --name-only --diff-filter=d | xargs bat --diff
   end

   # TODO
   # battail : tail -f /var/log/pacman.log | bat --paging=never -l log
   # batshow : git show v0.6.0:src/main.rs | bat -l rs
   # see https://github.com/sharkdp/bat

   #---------------------- powerline-status ---------------------
   # powerline-config path
   if test -d ~/.local/bin
      # Fedora Linux
      set -gx PATH ~/.local/bin $PATH 
   else if test -d ~/Library/Python/3.8/bin
      # Mac OS X
      set -gx PATH ~/Library/Python/3.8/bin $PATH
   end

   # powerline-status install path for python
   if test -d ~/.local/lib/python3.7/site-packages/powerline
      # Fedora Linux
      set POWER_LINE_PATH ~/.local/lib/python3.7/site-packages/powerline
   else if test -d ~/Library/Python/3.8/lib/python/site-packages/powerline
      # Mac OS X
      set POWER_LINE_PATH ~/Library/Python/3.8/lib/python/site-packages/powerline
   end
   set fish_function_path $fish_function_path $POWER_LINE_PATH/bindings/fish
   source $POWER_LINE_PATH/bindings/fish/powerline-setup.fish
   powerline-setup

   #---------------------- home brew ---------------------
   set -gx HOMEBREW_PREFIX "/home/linuxbrew/.linuxbrew";
   set -gx HOMEBREW_CELLAR "/home/linuxbrew/.linuxbrew/Cellar";
   set -gx HOMEBREW_REPOSITORY "/home/linuxbrew/.linuxbrew/Homebrew";
   set -gx PATH "/home/linuxbrew/.linuxbrew/bin" "/home/linuxbrew/.linuxbrew/sbin" $PATH;
   set -gx MANPATH "/home/linuxbrew/.linuxbrew/share/man" $MANPATH;
   set -gx INFOPATH "/home/linuxbrew/.linuxbrew/share/info" $INFOPATH;

   #---------------------- git ---------------------
	function gclone -d "Clone a git repository from Victory"
      set num (count $argv)
      if test $num = 1 
         set project $argv[1]
         command git clone athichart@victorybattleship.local:/Users/athichart/Google\ Drive/git/$project
      else
         echo "usage: gclone <repository>"
      end
   end  # funciton

   alias gts='git status'
   alias gtl='git log'
   alias gtpush='git push origin master'
   alias gtpull='git pull origin master'

   #---------------------- Aliases ---------------------
   alias clean='find . -type f \( -name ".*~" -o -name "*~" -o -name "a.out" -o -name "core" -o -name "*.pyc" -o -name "*.class" \) -delete'
   # Replacing ls with exa
   alias ls='exa --icons'
   # exa options : --extended --only-dirs
   alias ll='exa -aa -l -g -h --git --modified --time-style=long-iso -H --classify --icons'
   alias la='exa --icons -a'
   alias reload='source ~/.config/fish/config.fish'
   alias tl='tmux ls'
   alias ta='tmux attach -dt'
   alias vi='vim'

   #---------------------- Variables ---------------------
   set -gx PKG_CONFIG_PATH /usr/local/lib/pkgconfig $PKG_CONFIG_PATH 
   set -gx PATH "$HOME/bin" "$HOME/Workspace/scripts" $PATH;
   set -gx EDITOR vim
   set -gx VISUAL vim

   set -gx myver 1.5
   echo "Loading my fish startup script $myver"
   #neofetch
end
