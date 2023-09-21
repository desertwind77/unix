# Vim

Vim can have multiple tabs, each of which can be separated into multiple windows. Each window contains a buffer. Multiple windows may host the same buffere.

## Window
| Command | Function |
|---------|----------|
|:new|Create a new window|
|`Ctrl-w v` or :vsplit|Split window veritcally|
|`Ctrl-w s` or :split|Split window horizontally|
|`Ctrl-w Ctrl-r`|Swap the two parts of a split window|
|`Ctrl-w o`|Make the current window the only one on screen and close all others|
|`Ctrl-w w`|Move cursor to other window|
|`Ctrl-w h`|Move cursor left|
|`Ctrl-w l`|Move cursor right|
|`Ctrl-w j`|Move cursor down|
|`Ctrl-w k`|Move cursor up|
|:vertical sb 3|Split vertically and show buffer 3 on the left
|:vertical rightbelow sfind file.txt|Split vertically and show file.txt on the right|
|:rightbelow sfind file.txt|Split horizontally and show file.txt in the bottom|

## Buffer
| Command | Function |
|---------|----------|
|:new|Open an empty buffer|
|:ls, :buffers|List all the buffer|
|:bnext, :bn|Go to the next buffer|
|:bprev, :bp|Go to the previous buffer|
|:b `num`|Jump to the buffer `num` shown in :ls or :buffers|
|:b `filename`|Jump to the buffer `filename`|
|:bd `num`|Delete the current buffer or `num`|
|:bd!|Delete the current buffer and discard any changes|
|`Ctrl-o`, `Ctrl-i`|Jump history|
|`Ctrl-^`|Toggle between the current and the last buffer|

## Tab

| Command | Function |
|---------|----------|
|:tabedit `file`|Edit `file` in a new tab|
|:tabfind `file`|Search the path and open `file` in a new tab|
|:set path=.,,** |Set the search path for :tabfind. path is comma separated.<Br> <li>A single dot ('.') means the directory containing the file.<br> <li>An empty string means the current directory.<br> <li> ** means the directory under the current directory|
|:tab drop `file`|Jump to a window/tab containing the file if exists or open `file` in a new tab|
|:tab split|Copy the current window to a new tab}
|:tabclose|Close the current tab|
|:tabclose `i`|Close the ``i^th`` tab|
|:tabonly|Close all other tabs and show only the current tab|
|:tab ball|Show each buffer in a tab (up to 'tabpagemax' tabs)|
|:tab help|Open help in a new tab|
|:tabs|Show all tabs|
|:tabn [`tabno`]|Go to the next tab or `tabno`|
|:tabp|Go to the previous tab|
|:tabfirst|Go to the first tab|
|:tablast|Go to the last tab|
|:tabm 0|Move current tab to first|
|:tabm|Move current tab to last|
|:tabm `i`|Move current tab to the position ``(i+1)^{th}``|

To navigate between tabs in normal mode

| Command | Function |
|---------|----------|
|gt|Go to next tab|
|gT|Go to previous tab|
|`i`gt|Go to tab in the position ``i^{th}``|
|tc|tabclose|
|te|tabedit|
|tf|tabfirst|
|tl|tablast|
|tm|tabm|
|tn|tabnew|
|tp|tabprevious|

## Changing the case
| Command | Function |
|---------|----------|
|[num]~|Invert the case of the character under the cursor|
|g~ followed by motion|Invert the case of those characters e.g. g~e, g~$, g~iw, etc|
|gu followed by motion|Change those characters to lowercase e.g. gue, gu$, guiw, etc|
|gU followed by motion|Changes those characters to UPPERCASE e.g. gUe, gU$, gUiw, etc|

## Spelling
| Command | Function |
|---------|----------|
|]s|Move to the next misspelled word|
|[s|Move to the previous misspelled word|
|z=|Show suggestion|
|zg|Add the word to the dictionary|
|zw|Mark the word as incorrect|

## Textwrap
| Command | Function |
|---------|----------|
|\ + a|Toggle text wrap|
|gj|Go down one line in the wrapped line|
|gk|Go up one line in the wrapped line|
|g^|Go to the beginning of the wrapped line|
|g$|Go to the end of the wrapped line|

## cscope
| Command | Function |
|---------|----------|
|csa|cs add|
|csf|cs find|
|csk|cs kill|
|csr|cs reset|
|css|cs show|
|csh|cs help|

## ctags
1) Generate the tags file
```
ctags -R *
```
2) Using vim to search for a tag called title
```
vim -t title
```
3) Commands inside Vim

| Command | Functon |
|---------|---------|
|:tag `ClassName`|Search for the tag `ClassName`|
|:tn, :tnext|Go to the next definition|
|:tp, :tprevious|Go to the previous definition|
|:tf, :tfirst|Go to the first definition|
|:tl, :tlast|Go to the last definition|
|:ts, :tselect|List all definitions|

Placing the cursor on some text and then

| Command | Functon |
|---------|---------|
|Ctrl-]|Jump to the tag underneath the cursor|
|Ctrl-t|Jump back up in the tag stack e.g. from the definition|
|Ctrl-w}|Preview definition|
|g]|See all definitions|

## Miscellenous
| Command | Function |
|---------|----------|
|`Ctrl-w z`, `Ctrl-w Ctrl-z`,:pc[lose][!]|Close the preview window|
|:term|Run a terminal inside vim (from 8.1)|
|:!|Run the last external command|
|:!!|Repeat the last command|
|:!`command`|Run `command`|
|:silent `commad`|Eliminate the need to hit enter after `command` is done|
|:r!`command`|Run `command` and copy the result to a bufffer|
|:qa!, :qall!|Exit vim from split mode or tab|
|:e, :e!|Reload the file e.g. after removing the read-only permission so vim allow us to edit the file. `:e!` will discard all changes in the current window.|
|:v/`Warning`/p|Search for the lines not containing a pattern `Warning`|
|:vimgrep /0$/ example.txt|Search for lines ending with 0 in file example.txt|
|:cwin|Open quickfix window (window 4)|
|:help quickfix|Open help (window 1)|

### Wrap existing text at 80 characters
1) Set the textwidth to 80 by using `:set textwidth=80`
2) Apply automatically within certain file types like Markdown `au BufRead,BufNewFile *.md setlocal textwidth=80`
3) Select the lines to re-format by pressing `v` and then scroll to select the desired lines.
4) Reformat those lines by pressing `gq`

### Comment on a multi-line code snipplet without using nerdcommenter
1) go to the first line you want to comment, press `Ctrl+v`. This will put the editor in the VISUAL BLOCK mode.
2) Use the arrow key to select until the last line.
3) Press `Shift+i`, which will put the editor in INSERT mode and then press `#`. This will add a hash to the first line.
4) Press Esc (give it a second), and it will insert a `#` character on all other selected lines.

### Scroll the vim terminal window
1) To enter the normal mode which we can use with vim's normal navigation and search, press `Ctrl-\ Ctrl-n`
2) To return to the terminal mode, press `i` or `a`.

### Insert the same characters across multiple line
1) Move the cursor to the starting point on the first line
2) Enter the visual block mode with `Ctrl-v`
3) Press `j` three times or `3j` to jump down by 3 times or `G` to jump to the last line.
4) Press `I`
5) Type whatever change you want. Note that the change will appear only on the first line until `Esc` is press.
6) Press `Esc`. Then all lines will be updated.

## Leader Key Combination
| Command | Function |
|---------|----------|
|\ + a|Toggle text wrap|
|\ + b|Turn on tagbar|
|\ + c|Show list of opened buffers to choose from|
|\ + d|Show all the buffers|
|\ + h|Stop search highlight|
|\ + i|Toggle indent line|
|\ + l|Display location list [NOT WORKING]|
|\ + n|[nerdtree] Toggle nerdtree file browser and jump to it|
|\ + q|Display quickfix list|
|\ + s|Toggle spelling|
|\ + t|[nerdtree] Toggle nerdtree file browser|
|\ + u|Show undo tree|
|\ + w|Strip white spaces|
|\ + nn|Toggle line number|
|\ + \\ |[vim-easy-align] Align a markdown table after being selected in visual mode|

## Plugins
### CtrlP
**Use Cases** : switch to the desired file by filename matching  
Hit `Ctrl + P` and type a part of the filename, select a desired file and hit `Enter`.

| Command | Function |
|---------|----------|
|:CtrlP [`starting dir`]|Invoke CtrlP in find file mode|
|:CtrlPBuffer or :CtrlPMRU|Invoke CtrlP in find buffer/MRU mode|
|:CtrlPMixed|Search in Files, Buffers and MRU files at the same time|
|`Ctrl-p` in normal mode|Invoke CtrlPMixed|
|`Ctrl-p` in insert mode|Spelling suggestion|

Once CtrlP is open:

| Command | Function |
|---------|----------|
|`F5`|Purge the cache and reload the current directory|
|`Ctrl-d`|Switch to filename-only search instead of full path|
|`Ctrl-r`|Switch to regexp mode|
|`Ctrl-f Ctrl-b`|Cycle between mode|
|`Ctrl-j`, `Ctrl-k`, Up, Down|Navigate the result list|

- Use `Ctrl-t` or `Ctrl-v`, `Ctrl-x` to open the selected entry in a new tab or in a new split.
- Use `Ctrl-n`, `Ctrl-p` to select the next/previous string in the prompt's history.
- Use `Ctrl-y` to create a new file and its parent directories.
- Use `Ctrl-z` to mark/unmark multiple files and `Ctrl-o` to open them.

### nerdcommenter
| Command | Function |
|---------|----------|
|\ + cc|Comment out the current line or text selected in visual mode|
|\ + cn|Same as cc but forces nesting|
|\ + c + space|Toggles the comment state of the selected line(s). If the topmost selected line is commented, all selected lines are uncommented and vice versa.|
|\ + cm|Comments the given lines using only one set of multipart delimiters.|
|\ + ci|Toggles the comment state of the selected line(s) individually.|
|\ + cs|Comments out the selected lines with a pretty block formatted layout.|
|\ + cy|Same as cc except that the commented line(s) are yanked first.|
|\ + c$|Comments the current line from the cursor to the end of line.|
|\ + cA|Add comment delimiters to the end of line and goes into insert mode between them.|
|\ + ca|Switches to the alternative set of delimiters.|
|\ + cl or cb|Same as |NERDCommenterComment| except that the delimiters are aligned down the left side (<leader>cl) or both sides (<leader>cb).|
|\ + cu|Uncomments the selected line(s).|


### vim-expand-region
| Command | Function |
|---------|----------|
|+|Expand the selected region|
|-|Shrink the selected region|

### vim-surround
Change parentheses, brackets, quotes, HTML/XML tags. Note that we have to type the command when the cursor is inside the quotes, etc.

      initially      "Hello world!"
      cs"'           'Hello world!'
      cs'<p>         <p>Hello world!</p>
      cst"           "Hello world!"
      ds"            Hello world!

When the cursor is on `Hello`,

      ysiw]          [Hello] world!
      cs]{           { Hello } world!  or
      cs]}           {Hello} world!
      yssb or yss)   ({Hello} world!)
      ds{ds)         Hello world!
      ysiw<em>       <em>Hello</em> world!

Hold SHIFT and then press v and $ to enter linewise visual mode, press `S<p class="important">`
```
<p class="important">
    <em>Hello</em> world!
</p>
```
The . command will work with ds, cs, and yss if you install repeat.vim.

### vim-windowswap
Swap windows
1) Navigate to the window you'd like to move and press `leader ww`
2) Navigate to the window you'd like to swap with and Press `leader ww` again

