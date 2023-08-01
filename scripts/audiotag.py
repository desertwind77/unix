#!/usr/bin/env python3
'''
A script to automatically populate the metadata of audio files in the flac format

https://www.last.fm/api/webauth
https://www.geeksforgeeks.org/extract-and-add-flac-audio-metadata-using-the-mutagen-module-in-python/
https://mutagen.readthedocs.io/en/latest/
'''

from collections import defaultdict
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

class FileBase:
    def __init__( self, config ):
        self.config = config

    def sanitize_text( self, txt ):
        '''Change the text to conform with what is expected'''
        for replacement in self.config[ 'Cleanup' ][ 'Replaced Chars' ]:
            dst = replacement[ "dst"]
            for src in replacement[ "src" ]:
                txt = txt.replace( src, dst )
        # FIXME: skip Roman numbers
        # FIXME: capwords is not good
        #return string.capwords( txt )
        return txt

class Album( FileBase ):
    def __init__( self, config, path ):
        super().__init__( config )
        self.path = path
        self.disc = defaultdict( list )
        self.contents = []

    def add_track( self, flac ):
        self.contents.append( flac )
        if flac.discno:
            self.disc[ flac.discno ].append( flac )

    def album_name( self ):
        # All flac files in this album should have the same album name
        result = list( set( f.album for f in self.contents ) )
        if len( result ) == 1:
            return result[ 0 ]

        # Flac files have different album name. Usually, this is because
        # the disc number is a part of the album name. # Assume that the
        # longest common string is the album name
        min_len = min( len( a ) for a in result )
        stop = 0
        for i in range( min_len ):
            cur_char = set( a[ i ] for a in result )
            stop = i
            if len( cur_char ) != 1:
                break
        if stop != 0:
            return result[ 0 ][ : stop + 1 ]

        # If no album is present, try to get one from the
        # folder name.
        obj = re.match( r'(.*?) - (.*)', str( self.path.name ) )
        if obj:
            return obj.group( 2 )
        return None

    def album_artist( self ):
        # All flac files in this album should have the same
        # album artist
        result = set( f.album_artist for f in self.contents )
        assert len( result ) == 1
        result = list( result )[ 0 ]
        if result:
            return result

        # If no album artist is present, try to get one from the
        # folder name.
        obj = re.match( r'(.*?) - (.*)', str( self.path.name ) )
        if obj:
            return obj.group( 1 )
        return None

    def show_content( self ):
        print( f'Album Artist : {self.album_artist()}' )
        print( f'Album : {self.album_name()}' )

        if len( self.disc ) > 1:
            for disc, flacs in self.disc.items():
                print( f'Disc {disc}' )
                for flac in flacs:
                    print( f'   {flac.track:03} {flac.title}' )
        else:
            for flac in self.contents:
                print( f'{flac.track:03} {flac.title}' )

class FlacFile( FileBase ):
    def __init__( self, config, path ):
        super().__init__( config )
        self.path = path
        self.metadata = FLAC( self.path )
        self.track = self.get_track_number()
        self.title = self.get_title()
        self.artist = self.get_metadata_str( 'artist' )
        self.album = self.get_metadata_str( 'album' )
        self.album_artist = self.get_metadata_str( 'albumartist' )
        self.discno = self.get_disc_number()
        self.has_album_art = False

    def sanitize_number( self, txt ):
        if '/' in txt:
            txt = txt.split( '/' )
            return int( txt[ 0 ] )
        return int( txt )

    def get_metadata( self, field ):
        title = self.metadata.get( field )
        return title[ 0 ] if title else None

    def get_metadata_num( self, field ):
        result = self.get_metadata( field )
        return self.sanitize_number( result ) if result else None

    def get_metadata_str( self, field ):
        result = self.get_metadata( field )
        return self.sanitize_text( result ) if result else None

    def get_track_number( self ):
        track = self.get_metadata_num( 'tracknumber' )
        if track:
            return track

        filename = self.sanitize_text( str( self.path.name ) )
        obj = re.match( r'^(\d+) *(.*)', filename )
        if obj:
            return obj.group( 1 )
        return None

    def get_title( self ):
        title = self.get_metadata_str( 'title' )
        if title:
            return title

        filename = self.sanitize_text( str( self.path.name ) )
        obj = re.match( r'^(\d+) *(.*)', filename )
        if obj:
            return obj.group( 2 )
        return None

    def get_disc_number_from_metadata( self ):
        discno = self.get_metadata_num( 'discnumber' )
        return discno if discno else None

    def get_disc_number_from_path( self ):
        discno = None
        parent = self.path.absolute().parent.name
        obj = re.match( r'cd.*(\d+)', parent.lower() )
        if obj:
            discno = int( obj.group( 1 ) )
        else:
            obj = re.match( r'disc.*(\d+)', parent.lower() )
            if obj:
                discno = int( obj.group( 1 ) )
        return discno

    def get_disc_number( self ):
        # For Disc No, we trust the information from the path
        discno = self.get_disc_number_from_path()
        if not discno:
            discno = self.get_disc_number_from_metadata()
        return discno

    def get_album_art( self ):
        metadata = FLAC( self.path )
        for pic in metadata.pictures:
            if pic.type == 3:
                self.album_art = True
                break

    def has_required_tag( self ):
        return all( self.track, self.title, self.artist, self.album,
                    self.album_artist, self.discno, self.has_album_art )

    def album_path( self ):
        parent = self.path.absolute().parent
        if re.search( r'cd.*(\d+)', str( parent ).lower() ) or \
                re.search( r'disc.*(\d+)', str( parent ).lower() ):
            parent = parent.parent
        return parent

    def dump_metadata( self ):
        for tag, value in self.metadata.items():
            print( f'{tag} = {value}' )

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
    def __init__( self, location, config, params ):
        self.location = location
        self.config = config
        self.verbose = params.verbose
        self.dry_run = params.dry_run
        self.albums = {}
        self.unknown = []

    # def get_format( self, filename ):
    #     '''Determine the file format from the filename'''
    #     filename = str( filename.name )
    #     return os.path.splitext( filename )[ -1 ].lower()

    # def remove_unwanted_files( self ):
    #     '''Remove files of which format is not in the allowed list'''
    #     path = Path( self.folder )
    #     filenames = [ f for f in path.glob( '**/*' ) if os.path.isfile( f ) ]
    #     for filename in filenames:
    #         fmt = self.get_format( filename )
    #         if fmt not in self.config[ "Cleanup" ][ "Allowed Formats" ]:
    #             if self.verbose:
    #                 print( f'Removing {filename}' )
    #             if not self.dry_run:
    #                 os.remove( filenames )

    def load_flac_files( self ):
        cwd = Path( self.location )
        for filename in list( cwd.glob( '**/*.flac' ) ):
            flac = FlacFile( self.config, filename )
            if not flac.album:
                self.unknown.append( flac )
                continue
            if flac.album_path() not in self.albums:
                self.albums[ flac.album_path() ] = \
                        Album( self.config, flac.album_path() )
            self.albums[ flac.album_path() ].add_track( flac )

    def show_albums( self ):
        for album in self.albums.values():
            album.show_content()
            print()

    def run( self ):
        self.load_flac_files()
        self.show_albums()

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
        cmds = [ CleanupCmd( os.getcwd(), self.config, params ) ]
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
