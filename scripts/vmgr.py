#!/usr/bin/env python3
'''
vmgr : intsall, update, or uninstall vim plugins

This script must be running outside the .vim directory.
'''
from datetime import datetime
import argparse
import os
import shutil
import subprocess
# pylint: disable=import-error
from colorama import Fore, Style
from tabulate import tabulate
from genutils import load_config, check_if_folder_exists

CONFIG_FILENAME = 'config/vmgr.json'

class PluginConfigInfo:
    '''Information about vim plugins from the config'''
    def __init__( self, plugins, vim_dir, plugin_dir, git_repo ):
        self.plugins = plugins
        self.vim_dir = vim_dir
        self.plugin_dir = plugin_dir
        self.git_repo = git_repo

def load_vmgr_config( filename, verbose=False):
    '''Load the plugin configuration'''
    config = load_config( filename, verbose=verbose )
    plugins = config[ 'Plugins']
    vim_dir = config[ 'InstallInfo' ][ 'VimDir' ]
    plugin_dir = config[ 'InstallInfo' ][ 'PluginDir' ]
    git_repo = config[ 'InstallInfo' ][ 'GitRepo' ]
    return PluginConfigInfo( plugins, vim_dir, plugin_dir, git_repo )

def install_plugin( pinfo, force=False):
    '''Install all the plugins'''
    full_plugin_dir = os.path.join( pinfo.vim_dir, pinfo.plugin_dir )
    if not os.path.isdir( full_plugin_dir ) or force:
        if force:
            shutil.rmtree( pinfo.vim_dir )
        # os.makedirs() create a directory recursively while os.mkdir()
        # does not do recursively
        os.makedirs( full_plugin_dir )
    current_dir = os.getcwd()
    os.chdir( pinfo.vim_dir )

    # Initalize git repository
    if not os.path.isdir( pinfo.git_repo ):
        cmd = [ 'git', 'init' ]
        try:
            subprocess.run( cmd, stdout=subprocess.DEVNULL, check=True )
        except subprocess.CalledProcessError:
            print( 'Unable to initialize the git repository' )
            return

    # Install each plugin
    for name, data in pinfo.plugins.items():
        url = data[ 'URL' ]
        enable = ( data[ 'Enable' ] == 'True' )
        des = os.path.join( pinfo.plugin_dir, name )

        if not enable or os.path.isdir( des ):
            print( f'Skipped {name}' )
            continue

        cmd = [ 'git', 'submodule', 'add', url, des ]
        try:
            subprocess.run( cmd, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, check=True )
        except subprocess.CalledProcessError:
            print( f'Unable to install {name} with command:' )
            print_cmd = ' '.join( cmd )
            print( f'   {print_cmd}' )
            continue
        print( f'Installed {name}' )

    cmd = [ 'git', 'commit', '-m', 'Vim plugin installation' ]
    try:
        subprocess.run( cmd, stdout=subprocess.DEVNULL, check=True )
    except subprocess.CalledProcessError as exception:
        print( exception )

    os.chdir( current_dir )

def uninstall_plugin( pinfo, name ):
    '''Uninstall a specific plugin'''
    check_if_folder_exists( pinfo.vim_dir )
    check_if_folder_exists( os.path.join( pinfo.vim_dir, pinfo.plugin_dir, name ) )

    current_dir = os.getcwd()
    os.chdir( pinfo.vim_dir )
    des = os.path.join( pinfo.plugin_dir, name )

    cmds = [
            [ 'git', 'submodule', 'deinit', '--force', des ],
            [ 'git', 'rm', des ],
            [ 'git', 'commit', '-m', f'Removing {name}' ],
    ]

    for cmd in cmds:
        try:
            subprocess.run( cmd, stdout=subprocess.DEVNULL, check=True )
        except subprocess.CalledProcessError:
            print( f'Fatal error in uninstalling {name}' )
            print( f'   {cmd}' )
            os.chdir( current_dir )
            return

    git_dest = os.path.join ( pinfo.git_repo, 'modules', des )
    shutil.rmtree( git_dest )

    os.chdir( current_dir )

def update_plugin( pinfo ):
    '''Update all the plugins'''
    check_if_folder_exists( pinfo.vim_dir )
    current_dir = os.getcwd()
    os.chdir( pinfo.vim_dir )

    now = datetime.now()
    datetime_string = now.strftime( "%d/%m/%Y %H:%M:%S" )

    # Running either of these commands
    #     git submodule update --remote --merge
    #     git submodule update --init --recursive
    cmd = [ 'git', 'submodule', 'update', '--remote', '--merge' ]
    try:
        subprocess.run( cmd, stdout=subprocess.DEVNULL, check=True )
    except subprocess.CalledProcessError:
        print( 'Fatal error in updating plugins' )
        os.chdir( current_dir )
        return

    cmd = [ 'git', 'commit', '-a', '-m',
            f'"[{datetime_string}] Updating plugin"' ]
    try:
        subprocess.run( cmd, stdout=subprocess.DEVNULL, check=True )
    except subprocess.CalledProcessError:
        # Suppressing the exception on purpose because git commit may
        # return a non-zero code when there is nothing to commit.
        os.chdir( current_dir )

def show_plugin( pinfo ):
    '''Show all the plugins to be installed'''
    tab_header = [ 'Plugin', 'Enable', 'Description' ]
    tab_width = [ None, 6, 40 ]
    tab_data = []
    for name, data in pinfo.plugins.items():
        desc = data[ 'Desc' ]
        enable = ( data[ 'Enable' ] == 'True' )
        tab_data.append( [ name, enable, desc ] )

    print( tabulate( tab_data, headers=tab_header,tablefmt="rounded_grid",
                     maxcolwidths=tab_width ) )

def parse_argv():
    '''Parse the command line arguments'''
    parser = argparse.ArgumentParser( description='vim plugin manager' )
    parser.add_argument( '-v', '--verbose', action='store_true', dest='verbose',
                         help='Print log message' )

    subparser = parser.add_subparsers( dest='command' )
    subparser.required = True

    subparser.add_parser( 'show', help='Show all vim plugins to be installed' )

    install_parser = subparser.add_parser( 'install',
                                           help='Install all vim plugins' )
    install_parser.add_argument( '-f', '--force',
                                 action='store_true', dest='force' )

    subparser.add_parser( 'update', help='update all vim plugins' )

    uninstall_parser = subparser.add_parser( 'uninstall',
                                             help='Uninstall vim plugin' )
    uninstall_parser.add_argument( 'name', action='store',
                                    help='plugin to be uninstalled' )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_argv()
    plugin_info = load_vmgr_config( CONFIG_FILENAME, verbose=args.verbose )

    if args.command == 'install':
        install_plugin( plugin_info, args.force )
    elif args.command == 'uninstall':
        uninstall_plugin( plugin_info, args.name )
    elif args.command == 'update':
        update_plugin( plugin_info )
    elif args.command == 'show':
        show_plugin( plugin_info )

    print( f'{Fore.GREEN}Success{Style.RESET_ALL}' )
