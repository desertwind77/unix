# MacOS

## Change the default shell to fish
1) Adding `python` to `$PATH` in `$HOME/.local/share/omf/pkg/powerline/init.fish` for example:
```
set -gx PATH "/Library/Frameworks/Python.framework/Versions/3.10/bin" "$PATH"
```
2) Append `/opt/homebrew/bin/fish` to `/etc/shell`
3) `chsh -s /opt/homebrew/bin/fish`

## To enable/disable FTP
    sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist
    sudo -s launchctl unload -w /System/Library/LaunchDaemons/ftp.plist

## To enable/disable SSH/SFTP
System Preferences > Sharing > Remote Login

## Print screen on Mac
`Cmd + shift + 3` captures the whole screen
`Cmd + shift + 4` captures select area by dragging mouse
`Cmd + shift + 4 + spacebak` captures select the window

## Convert from TIS-620 (Thai language) to UTF-8 encoding
    # show all supported encoding.
    iconv -l
    iconv -f tis-620 -t utf-8 source.xml > destination.xml

## Create .iso file
1) Use DiskUtility to create .dmg. Then use DiskUtility to convert from .dmg to .cdr.
2) Convert .cdr to .iso
```
hdiutil makehybrid -iso -joliet -o [filename].iso [filename].cdr
```
or
```
hdiutil convert /path/imagefile.cdr -format UDTO -o /path/convertedimage.iso
```

## Mount .iso file
1) DiskUtility > File > Open Disk Image
2) `hdiutil mount file.iso`

## Show and update macOS System Updates
    softwareupdate -l
    sudo softwareupdate -iva

## Show and update software downloaded from Mac App Store
Install mas via brew

    brew install mas

Show all applications installed via AppStore

    mas list

Show all outdated apps

    mas outdated

Upgrade all outdated apps

    mas upgrade

Search for an app

    mas search <name>

Install an app. `app_number` is from the output of `mas search`

    mas install <app_number>

## Fixing Rocksmith Real Tone cable in Steam
Changing from `RealToneCableOnly=0` in `Rocksmith.ini` to `RealToneCableOnly=1`