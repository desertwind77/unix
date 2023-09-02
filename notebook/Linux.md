# Linux

## Configuration after installation
### 1. Set hostname

    hostnamectl set-hostname <new hostname>

### 2. Configure firewall
```
echo '<?xml version="1.0" encoding="utf-8"?>
<service>
short>MOSH</short>
description>Mosh (mosh.mit.edu) is a free replacement for SSH that allows roaming and        supports intermittent connectivity.</description>
port protocol="udp" port="60001-60100"/>
</service>' > /etc/firewalld/services/mosh.xml

systemctl enable sshd
systemctl start sshd
systemctl enable mariadb
systemctl start mariadb
systemctl enable httpd
systemctl start httpd
    
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-service=mosh
    
# For Roon Server, if installed on Linux
firewall-cmd --permanent --zone=public --add-port=9003/udp
firewall-cmd --permanent --zone=public --add-port=9100-9200/tcp
    
# For Grafana
firewall-cmd --permanent --zone=public --add-port=3000/tcp
    
firewall-cmd --reload
```

### 3. Wordpress
#### 3.1 Configure permission for wordpress
    setsebool -P httpd_can_network_connect=1
    setsebool -P httpd_can_network_connect_db=1
    setsebool -P httpd_can_sendmail=1
    chown -R apache.apache /usr/share/wordpress/
    chcon -Rv --type=httpd_sys_rw_content_t /usr/share/wordpress
      
#### 3.2 Create Wordpress database
    sudo mysqladmin -u root password
    sudo mysqladmin create wannawalkwithmedb -u root -p
    sudo mysql -D mysql -u root -p
    GRANT ALL PRIVILEGES ON wannawalkwithmedb.* To 'wannawalkwithme'@'localhost' IDENTIFIED BY '2520MagellaN';
    FLUSH PRIVILEGES;
    QUIT;
    
### 4. Disable SELINUX

### 5. Enable mDNS
#### 5.1 Configure firewall
    sudo firewall-cmd --permanent --add-service=mdns
    sudo firewall-cmd --reload

#### 5.2 Configure systemd-resolved
    sudo mkdir -p /etc/systemd/resolved.conf.d
    sudo tee /etc/systemd/resolved.conf.d/00-custom.conf << EOF > /dev/null
    [Resolve]
    MulticastDNS=yes
    EOF
    sudo systemctl restart systemd-resolved.service

#### 5.3 Configure NetworkManager
    sudo tee /etc/NetworkManager/conf.d/00-custom.conf << EOF > /dev/null
    [connection]
    connection.mdns=2
    EOF
    sudo systemctl restart NetworkManager.service

### 6 Configure fish shell
The `fish` shell itself will be installed via brew

#### 6.1 Install Oh My Fish!
    curl -L https://get.oh-my.fish | fish
    omf install powerline
    pip3 install powerline-status

Using omf

    omf list
    omf theme
    omf install agnoster
    omf theme agnoster

## Miscelleneous
### Secure shell without password
1) Generate public and private keys on the client

```
ssh-keygen -t rsa
```
   
2) Copy the public key to the git server
```
ssh-copy-id athichart@victorybattleship.local
```

### Configure Network Services to Auto Start on Boot
1) See if it is systemd or sysvinit
```
ps --pid 1
```
If it shows systemd, then it is a systemd-based system. if it shows init, it is a sysvinit-based system.

2) Enable/disable service and list the services

For systemd
```
systemctl enable/disable [service]
systemctl list-unit-files --state=disabled/enabled
```
For sysvinit
```
chkconfig --level AB [service] on/off
chkconfig --list
```

### Determine what services are running on what ports
#### Option 1 : netstat
```
netstat -ltnp | grep ':8081'
(Not all processes could be identified, non-owned process info will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN
```
where 
`-l` tells netstat to only show listening sockets.
`-t` tells it to display tcp connections.
`-n` instructs it show numerical addresses.
`-p` enables showing of the process ID and the process name.

#### Option 2 : lsof
```
sudo lsof -i :8081

COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
motion  10669 root    5u  IPv4  94740      0t0  TCP *:tproxy (LISTEN)
```
#### Option 3 : fuser
```
sudo fuser 8081/tcp
8081/tcp:            10669
ps -p 10669 -o comm=motion
```

### diff and patch two directories
    diff -ruN orig/ new/ > file.patch
where     
`-r` means recursive, so do subdirectories
`-u` means unified style, if your system lacks it or if recipient may not have it, use `-c`
`-N` means treat absent files as empty

To recreate the new folder from old folder and patch file, move the patch file to a directory where the orig/ folder exists. This folder will get clobbered, so keep a backup of it somewhere, or use a copy.

    patch -s -p0 < file.patch

where
`-s` means silent except errors
`-p0` is needed to find the proper folder
         
At this point, the orig/ folder contains the new/ content, but still has its old name.

### ctags
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
|^]|Jump to definition|
|^t|Jump back from definition|
|^w}|Preview definition|
|g]|See all definitions|

### Shell Scripts
#### Loop
bash
```
for i in 1, 2, 3, 4, 5
do
    echo $i
done

for i in {1..5} ; do echo $i; done

for i in {0..10..2} ; do echo $i; done

for i in $(unix-command-here) ; do echo $i; done
```
fish
```
for i in foo bar baz; echo $i; end
```

### cscope
#### Generate the cscope.files
```
# Linux kernel
LNX=/home/jru/linux-2.4.18
cd /
find  $LNX                                                            \
-path "$LNX/arch/*" ! -path "$LNX/arch/i386*" -prune -o               \
-path "$LNX/include/asm-*" ! -path "$LNX/include/asm-i386*" -prune -o \
-path "$LNX/tmp*" -prune -o                                           \
-path "$LNX/Documentation*" -prune -o                                 \
-path "$LNX/scripts*" -prune -o                                       \
-path "$LNX/drivers*" -prune -o                                       \
-name "*.[chxsS]" -print > /path/to/cscope.files
```
```
# Java
find /my/project/dir -name '*.java' > /path/to/cscope.files
```
#### Generate the cscope database
    cd /path/to
    cscope -b -q -k
    
#### Use cscope
    cd /path/to
    cscope -d

### Benchmark HDD or SSD performance
To show sequential latency

    ioping - R /dev/sda

To determine the latency of the entire drive

    ioping -c 10 /

### Convert a nero image to an iso image

    # Skip the first 300 bytes which are is nero header
    dd bs=1k if=image.nrg of=image.iso skip=300

### Convert img to VirtualBox hard drive
    VBoxManage convertfromraw --format VDI PlexMediaPlayer-1.3.5.723-a36fa532.Generic-x86_64.img plex.vdi

### Extract a .rpm file without installing it
    rpm2cpio file.rpm | cpio -idmv

### ls
`-lt` means sort by time
`-ltr` means sort by time in reverse order
`-S` means sort by size
`-h` means human-readable
`-R` means recursive

### Removing Windows linebreak (^M)
    tr -d '\15\32' <input> <output>
Or using the following command in Vim. Note that press Ctrl-v + Enter or Ctrl-v + Ctrl-M to type ^M.

    :1,$s/^M//g
or

    :set ff=unix or ff=dos

### Modify grub parameters to rotate screen
    grubby --args="fbcon:rotate=3" --update-kernel=ALL

Reference [1](https://docs.fedoraproject.org/en-US/fedora/rawhide/system-administrators-guide/kernel-module-driver-configuration/Working_with_the_GRUB_2_Boot_Loader/), [2](https://wiki.gentoo.org/wiki/Tallscreen_Monitor)

### Midnight Commander
|Command|Function|
|-------|--------|
|Ctrl-T|select a file|
|Shift-8,=,-|for *, +, -, respectively|
|Shift-<up/down>||

### Set time limit for a command
    timelimit <limit> <cmd>
where m, h, and d means mins, hours, and days, respectively.

### Rapidly invoke an editor to write a long, complex, or tricky command
In bash,

    fc
or

    Ctrl-x e

If prefer to use ESC-v instead of Ctrl-x e, set -o vi.

In fish, hold `ESC` and press `e` or `v`. To change the key binding to `ALT e` or `ALT v`, go to Preferences > Profiles > Keys in iterm2 and change left and right alt key behavior to Esc+.

### Copy file across machines
#### 1 Using `scp`
    scp -r <host@machine_name:from_remote_directory_path> <to_local_directory_path>

#### 2 Use `sftp -r <dir>` to copy the whole directory

#### 3 Using ssh and tar

    tar cf - -S -C <dir1> --exclude=<dir> <file list> | pigz | ssh <remotehost> "pigz -d | tar xvf - -S -C <dir2>"
or

    ssh <remotehost> "tar cf - -S -C <dir1> --one-file-system --numeric-owner <file list>  | pigz" > root.tgz
or

    ssh <remotehost> "tar cf - -S -C <dir1> <file list> | pigz" | pigz -d | tar xf - -S -C <dir2>

where
`<dir1>` : change to dir1 before performing tar
`<dir2>` : change to dir2 before performing untar
`-S` : handle sparse files efficiently (not supported on Mac)
`--numeric-owner` : always use numbers for user/group names
`--one-file-system` : stay in local file system when creating archive
`pigz` : compress/uncompress with gzip

#### 4 Using [rsync](https://www.cyberciti.biz/tips/linux-use-rsync-transfer-mirror-files-directories.html)

#### 5 Using sshfs
After installing sshfs, mount a remote directory with the following command

    sshfs user@server.com:/remote/dir /home/user/testdir

Unmount after finishing copy

    fusermount -u /home/user/testdir
    umount mountpoint
    diskutil unmount mountpoint      # Mac only

### [Cheat sheet](https://github.com/chubin/cheat.sh)
    curl cheat.sh

### Modern command line tools
| Command | Unix tools | Comment |
|---------|------------|---------|
|bandwhich||Display the current network utilization by process|
|bat|cat||
|dust|du||
|exa|ls|`exa --icons`|
|fd|find|`fd PATTERN` v.s. `find -iname '*PATTERN*'`|
|grex||Generate regular expression e.g. `grex -r f foo fooo` will give `^f(?:o{2,3})?$`|
|hyperfine|time|A command-line benchmarking tool|
|procs|ps||
|ripgrep|grep|`rg emacs .` will recursively search for the pattern|
|sd|sed|`sd emacs vim` v.s. `sed s/emacs/vim/g`|
|starsihp|bash||
|tealdeer|tldr||
|tokei||Display the statistics about the code|
|ytop|top||
|zoxide|cd|A very fast autojumper (need to spend time on this)|

### Executing a command on all files in a directory
```
find /some/directory -maxdepth 1 -type f -exec cmd option {} \;
```
* `-maxdepth 1` argument prevents find from recursively descending into any subdirectories.
* `-type -f` specifies that only plain files will be processed.
* `-exec cmd option {}` tells it to run cmd with the specified option for each file found, with the filename substituted for {}
* `\;` denotes the end of the command.

When I tried to construct the output filename from the input filename using [bash parameter expansion](http://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html), as follows, I was not happy. So I decided to write a python script to do that.

```
filename=$(basename -- "$fullfile")
extension="${filename##*.}"
filename="${filename%.*}"

or 

filename="${fullfile##*/}"

for f in *.gba ; do zip "${f%.*}".zip "$f"; done
``` 

### Display a markdown file in the terminal
```
glow -w 100 readme.md
```

## Docker
   1) command-line completion for fish
      Ref: https://docs.docker.com/docker-for-mac/#install-shell-completion

      mkdir -p ~/.config/fish/completions
      ln -shi /Applications/Docker.app/Contents/Resources/etc/docker.fish-completion ~/.     config/fish/completions/docker.fish
      ln -shi /Applications/Docker.app/Contents/Resources/etc/docker-compose.fish-completion ~/.config/fish/completions/docker-compose.fish

   2) Misc command
      docker version
      docker info
      docker container run --publish 8080:80 --name webhost --detach nginx
      docker container ls [-a]
      docker container stop <id>
      docker container logs webhost
      docker container top webhost
      docker container rm <list of id>
   3) tutorial
      docker run --name repo alpine/git clone https://github.com/docker/getting-started.git
      docker cp repo:/git/getting-started/ .
      cd getting-started
      docker build -t docker101tutorial .
      docker run -d -p 80:80 --name docker-tutorial docker101tutorial
      docker tag docker101tutorial athichart/docker101tutorial
      docker push athichart/docker101tutorial

## VS Code
### Extension
| Extension | Functionality |
|-----------|---------------|
| Code Runner | Running the program by clicking `play` button |

### 1. Shortcuts
|Command|Function|
|-------|--------|
|`Cmd + b`|Toggle sidebar|
|`Cmd + ,`|Open Setting|
|`Cmd + Shift + d`|Go to debug sidebar|
|`Cmd + Shift + e`|Go to file explorer sidebar|
|`Cmd + Shift + f`|Go to search sidebar|
|`Ctrl + Shift + g`|Go to source control sidebar|
|`Cmd + ,`|Go to setting e.g. font-ligatures, zoom, word wrap, exclude|
|`Ctrl +` `|Toggle the terminal window|
|`Ctrl + Cmd + up/down`|Increase/decrease the size of the terminal window|
|`Cmd + Shift + p`|Command palette (search for commands that can be run in VScode e. g. zen mode)|
|`Cmd + z`|Undo|
|`Cmd + d`|Select the word under cursor|
|`Cmd + f`|Search|
|`Cmd + w`|Close the file|
|`Cmd + p`|Search and open the file|
|`Ctrl + [shiTf] + tab`|Toggle through tabs|
|`Opt + < or >`|Go to next or prev word|
|`Cmd + < or >`|Go to the beginning or end of the line|
|`Cmd + up or down`|Go to the beginning or end of the file|

### 2. Features

|Feature|Function|
|-------|--------|
|emmet|generate html/css snipplet using short codes|



## Systemd
### 1. Service Configuration
	
Enable or disable a service to allow it to starts at boot time or not

	systemctl enable sshd.service
	systemctl disable sshd.service

Start, stop, restart or reload a service where reload means to reload the configuration file without restarting the service
	
	systemctl start sshd.service
	systemctl stop sshd.service	
	systemctl restart sshd.service
	systemctl reload sshd.service

Mask and unmask a service to prevent it from running either automatically or manually.
	
	sudo systemctl mask nginx.service
	sudo systemctl unmask nginx.service

Check status of a service

	systemctl cat atd.service
	systemctl list-dependencies sshd.service
	systemctl show sshd.service
	systemctl status sshd.service
	systemctl is-active sshd.service
	systemctl is-enabled sshd.service
	systemctl is-failed sshd.service

Add a new service to system

	cd /etc/systemd/system
	sudo ln -s /home/pi/gopigo_robot/remotecontrol.service
	sudo ln -s /home/pi/gopigo_robot/robot.service robot.service

An example from remotecontrol.service

    # /lib/systemd/system/remotecontrol.service
    [Unit]
    Description=RemoteControl Service
    After=bluetooth.service

    [Service]
    WorkingDirectory=/home/pi/gopigo_robot
    User=pi
    Type=simple
    ExecStart=/home/pi/gopigo_robot/RemoteControl.py

    [Install]
    WantedBy=multi-user.target

### 2. Show
List all loaded systemd units including services

    systemctl
	
List all systemd units

    systemctl --all
	
List all systemd units file

    systemctl list-unit-files
	
Lis all loaded services

    systemctl list-units --type=serivce
or

    systemctl --typeservice
	
List all loaded but active services

    systemctl list-units --type=serivce --state=active
or

    systemctl --typeservice --state=active
	
List all running services

    systemctl list-units --type=service --state=running 
or

    systemctl --type=service --state=running
	
Show the port a daemon process is listening on

    netstat
or

    ss -ltup
	
where the flag -l means print all listening sockets, -t displays all TCP connections, -u shows all UDP connections, -n means print numeric port numbers (instead of application names) and -p means show application name.

List the services or ports allowd by the firewall

    firewall-cmd --list-services
    firewall-cmd --list-ports

Reference : [1](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
	
