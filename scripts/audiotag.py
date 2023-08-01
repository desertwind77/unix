#!/usr/bin/env python3
'''
A script to automatically populate the metadata of audio files in the flac format

https://www.last.fm/api/webauth
https://www.geeksforgeeks.org/extract-and-add-flac-audio-metadata-using-the-mutagen-module-in-python/
https://mutagen.readthedocs.io/en/latest/
'''

from concurrent.futures.process import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
import argparse
import concurrent
import errno
import os
import re
import shutil
import string

# pylint: disable=import-error
from fastprogress import progress_bar
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType
from mutagen.wave import WAVE
from pydub import AudioSegment
from pydub.utils import mediainfo
import pyunpack

from genutils import load_config

CONFIG_FILENAME = "config/audiotag.json"

class UnsupportedFormat( Exception ):
    '''Unsupport Audio Format'''

class UnsupportedCommand( Exception ):
    '''Unsupport Command'''

@dataclass
class Parameters:
    '''Commandline parameters'''
    command : str
    dry_run : bool
    seq_exec : bool
    verbose : bool
    extract_dst : str
    archive_dst : str

class Folder:
    def remove_unwanted_files( self ):
        pass

class Album( Folder ):
    def __init__( self, location ):
        self.location = location
        self.album_name = None
        self.contents = []
        self.multidisc = False

        self.load_contents()

    def load_contents( self ):
        contents = os.listdir( self.location )

        folders = [ f for f in contents if os.path.isdir( f ) ]
        for folder in folders:
            obj = re.match( r'^cd.*(\d+).*', folder.lower() )
            if not obj:
                obj = re.match( r'^disc.*(\d+).*', folder.lower() )
            if obj:
                self.multidisc = True
                num = int( obj.group( 1 ) )
                path = os.path.join( self.location, folder )
                self.contents.append( Disc( path, num, self ) )

        flacs = [ f for f in contents if f.endswith( '.flac' ) ]
        if self.multidisc and flacs:
            # Files not in Disc
            raise Exception
        self.contents = [ FlacFile( os.path.join( self.location, f ), self )
                          for f in flacs ]

class Disc( Folder ):
    def __init__( self, location, disc_num, parent ):
        self.location = location
        self.disc_num = disc_num
        self.parent = parent
        self.contents = [ FlacFile( os.path.join( self.location, f ), self )
                          for f in os.listdir( self.location )
                          if f.endswith( '.flac' ) ]

class FlacFile:
    def __init__( self, location, parent ):
        #tag_list = [ 'title', 'artist', 'album', 'albumartist', 'tracknumber', 'discnumber'  ]
        self.location = location
        self.parent = parent
        self.metadata = FLAC( self.location )
        self.track = self.metadata.get( 'tracknumber' )
        self.title = self.metadata.get( 'title' )
        self.artist = self.metadata.get( 'artist' )
        self.album = self.metadata.get( 'album' )
        self.albumartist = self.metadata.get( 'albumartist' )
        self.disc_no = self.metadata.get( 'discnumber' )
        # if no disc_no, get from the parent or use pathlib
        # has album art

    def missing_required_tag( self ):
        pass

    def cleanup_track( self ):
        pass

    def cleanup_disc_no( self ):
        pass

class BaseCmd:
    '''The base class of all commands'''
    def run( self ):
        '''A virtual function to run the core function of the command'''

    def check_exist( self, filename ):
        '''Check if a file or a folder exists'''
        if not os.path.exists( filename ):
            raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT),
                                     filename )


class ExtractCmd( BaseCmd ):
    '''The command to extract a compressed file'''
    def __init__( self, filename, params ):
        self.filename = filename
        self.extract_dst = params.extract_dst
        self.archive_dst = params.archive_dst
        self.verbose = params.verbose
        self.dry_run = params.dry_run

    def run( self ):
        '''
        Extract an file to the destination folder and move the original file
        to the archive folder.
        '''
        try:
            self.check_exist( self.filename )
            if self.verbose:
                print( f'Extracting {self.filename}' )
            if self.dry_run:
                return
            pyunpack.Archive( self.filename ).extractall( self.extract_dst )
            shutil.move( self.filename, self.archive_dst )
        except ( pyunpack.PatoolError, FileNotFoundError ) as exception:
            print( exception )

class ConvertCmd( BaseCmd ):
    '''Convert an audio file into .flac'''
    def __init__( self, filename, params ):
        self.filename = filename
        self.verbose = params.verbose
        self.dry_run = params.dry_run

        self.format = self.get_format()
        self.tags = self.get_tags()
        self.album_art = self.get_album_art()

    def get_format( self ):
        '''Determine the file format from the filename'''
        filename = str( self.filename.name )
        ext = os.path.splitext( filename )[ -1 ].lower()
        if ext == '.wav':
            return 'wav'
        raise UnsupportedFormat( self.filename )

    def get_tags( self ):
        '''Get ID3 tags from the audio file'''
        return mediainfo( str( self.filename ) ).get( 'TAG', {} )

    def get_album_art( self ):
        '''Return the album art stored in the file'''
        if self.format == 'wav':
            metadata = WAVE( self.filename )
        else:
            raise UnsupportedFormat( self.filename )

        apic = metadata.tags.get( 'APIC:' )
        if not apic:
            return None

        pic = Picture()
        pic.type = PictureType.COVER_FRONT
        pic.desc = 'Front cover'
        pic.data = apic.data
        pic.mime = "image/jpeg"
        return pic

    def get_flac_filename( self ):
        '''Given a filename, change the file extension to .flac'''
        filename = self.filename.name
        ext = os.path.splitext( filename )[ -1 ]
        return str( self.filename ).replace( ext, '.flac' )

    def run( self ):
        try:
            self.check_exist( self.filename )
            dst = self.get_flac_filename()

            if self.verbose:
                print( f'Converting {self.filename}' )
            if self.dry_run:
                return

            audio = AudioSegment.from_file( self.filename, format=self.format )
            audio.export( dst, format="flac", tags=self.tags )

            album_art = self.get_album_art()
            if album_art:
                flac = FLAC( dst )
                flac.add_picture( album_art )
                flac.save()
        except ( FileNotFoundError ) as exception:
            print( exception )

class CleanupCmd( BaseCmd ):
    '''Command to do various cleanup'''
    def __init__( self, folder, config, params ):
        self.folder = folder
        self.config = config
        self.verbose = params.verbose
        self.dry_run = params.dry_run

    def contain_flac_files( self ):
        '''Check if this folder contains any flac files'''
        folder_path = Path( self.folder )
        all_flacs = list( folder_path.glob( '**/*.flac' ) )
        return bool( all_flacs )

    def get_format( self, filename ):
        '''Determine the file format from the filename'''
        filename = str( filename.name )
        return os.path.splitext( filename )[ -1 ].lower()

    def sanitize_text( self, txt ):
        '''Change the text to conform with what is expected'''
        for replacement in self.config[ 'Cleanup' ][ 'Replaced Chars' ]:
            dst = replacement[ "dst"]
            for src in replacement[ "src" ]:
                txt = txt.replace( src, dst )
        # FIXME: skip Roman numbers
        return string.capwords( txt )

    def sanitize_folder_name( self ):
        '''Change the folder name if need be'''
        new_name = self.sanitize_text( self.folder )
        if new_name != self.folder:
            if self.verbose:
                print( f'Renaming {self.folder} to {new_name}' )
            if not self.dry_run:
                os.rename( self.folder, new_name )
                self.folder = new_name

    def remove_unwanted_files( self ):
        '''Remove files of which format is not in the allowed list'''
        path = Path( self.folder )
        filenames = [ f for f in path.glob( '**/*' ) if os.path.isfile( f ) ]
        for filename in filenames:
            fmt = self.get_format( filename )
            if fmt not in self.config[ "Cleanup" ][ "Allowed Formats" ]:
                if self.verbose:
                    print( f'Removing {filename}' )
                if not self.dry_run:
                    os.remove( filenames )

    def sanitize_filenames( self ):
        # Capitalize the folder
        # Capitalize CD and Disc
        # Capitalize all files
        pass

    def sanitize_tags( self ):
        path = Path( self.folder )
        for filename in path.glob( '**/*.flac' ):
            metadata = FLAC( filename )

            tag_list = [ 'title', 'artist', 'album', 'tracknumber', 'discnumber'  ]
            print( metadata.keys() )
            for key in tag_list:
                value = metadata.get( key )
                if not value:
                    continue
                print( f'{key} = {value}' )

    def run( self ):
        if not self.contain_flac_files():
            return
        self.sanitize_folder_name()
        self.remove_unwanted_files()
        self.sanitize_filenames()
        self.sanitize_tags()

def execute( cmd ):
    '''Execute a command'''
    cmd.run()

class AudioTag:
    '''The main class for our Audio file tagging program'''
    def __init__( self, config_filename ):
        self.config = load_config( config_filename )

    def execute_commands( self, func, cmds, seq_exec=False ):
        '''Execute the command in the command list'''
        cpu_count = os.cpu_count()
        size = len( cmds )
        using_sequential_execution = seq_exec or cpu_count < 2 or size < 2

        if using_sequential_execution :
            for cmd in cmds:
                func( cmd )
        else:
            # Turning the verbose flag off cause it does not play well with progress bar
            new_cmds = [ cmd._replace( verbose=False ) for cmd in cmds ]
            print( *( cmd for cmd in new_cmds ), sep='\n' )
            with ProcessPoolExecutor( max_workers=cpu_count ) as executor:
                tasks = [ executor.submit( func, c ) for c in new_cmds]
                for _ in progress_bar( concurrent.futures.as_completed( tasks ), total=size ):
                    pass

    def extract_archives( self, params ):
        '''Extract all archives'''
        cwd = Path( os.getcwd() )
        cmds = []
        for fmt in self.config[ "Extract" ][ "Archive Format" ]:
            cmds += [ ExtractCmd( f, params ) for f in cwd.glob( f'**/*{fmt}' ) ]
        if cmds  and not params.dry_run:
            os.makedirs( 'archives' )
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec )

    def convert_audio( self, params ):
        '''Convert the autio files to .flac'''
        cwd = Path( os.getcwd() )
        cmds = []
        for fmt in self.config[ "Extract" ][ "Convert Format" ]:
            cmds += [ ConvertCmd( f, params ) for f in cwd.glob( f'**/*{fmt}' ) ]
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec )

    def cleanup( self, params ):
        '''Do various data cleanup on all folders in the current folder'''
        folders = os.listdir( '.' )
        cmds = [ CleanupCmd( f, self.config, params ) \
                 for f in folders if os.path.isdir( f ) ]
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec )

    def run( self, params ):
        '''Run the autio tag process'''
        if params.command == 'extract':
            self.extract_archives( params )
        elif params.command == 'convert':
            self.convert_audio( params )
        elif params.command == 'cleanup':
            self.cleanup( params )
        else:
            raise UnsupportedCommand( params.command )

def process_arguments():
    '''Process commandline arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument( '-d', '--dry-run', action='store_true', dest='dry_run',
                         help='Dry run' )
    parser.add_argument( '-s', '--seq-exec', action='store_true', dest='seq_exec',
                         help='Use sequential execution' )
    parser.add_argument( '-v', '--verbose', action='store_true', dest='verbose',
                         help='Print debug info' )

    subparser = parser.add_subparsers( dest='command' )
    subparser.required = True

    extract_parser = subparser.add_parser( 'extract', help='Extract compressed archives' )
    extract_parser.add_argument( '-a', '--archive-dst', default='archives',
                                 help='Move the uncompressed archives to this location' )
    extract_parser.add_argument( '-e', '--extract-dst', default='.',
                                 help='Extract the archives at this location' )

    subparser.add_parser( 'convert', help='Convert audio files to .flac' )
    subparser.add_parser( 'cleanup', help='Do various data cleanup' )

    args = parser.parse_args()
    seq_exec = False if args.command == 'cleanup' else args.seq_exec
    archive_dst = getattr( args, 'archive_dst', None )
    extract_dst = getattr( args, 'extract_dst', None )
    return Parameters( args.command, args.dry_run, seq_exec, args.verbose,
                       archive_dst, extract_dst )

def main():
    '''The main function'''
    audiotag = AudioTag( CONFIG_FILENAME )
    params = process_arguments()
    audiotag.run( params )

if __name__ == '__main__':
    main()
