#!/usr/bin/env python3
'''
A script to automatically populate the metadata of audio files in the flac format

https://www.last.fm/api/webauth
https://www.geeksforgeeks.org/extract-and-add-flac-audio-metadata-using-the-mutagen-module-in-python/
https://mutagen.readthedocs.io/en/latest/
'''

from collections import defaultdict
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
import argparse
import concurrent
import errno
import os
import re
import shutil
import subprocess

# pylint: disable=import-error
from fastprogress import progress_bar
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType
from mutagen.wave import WAVE
from pydub import AudioSegment
from pydub.utils import mediainfo
from tabulate import tabulate
import pyunpack

from genutils import load_config

CONFIG_FILENAME = "config/audiotag.json"

class UnsupportedFormat( Exception ):
    '''Unsupport Audio Format'''

class UnsupportedCommand( Exception ):
    '''Unsupport Command'''

class Parameters:
    '''Commandline parameters'''
    def __init__( self, params ):
        self.params = params

    def command( self ):
        '''Return the command argument'''
        return self.params.get( 'command' )

    def dry_run( self ):
        '''Return the dry_run argument'''
        return self.params.get( 'dry_run' )

    def seq_exec( self ):
        '''Return the seq_exec argument'''
        return self.params.get( 'seq_exec' )

    def verbose( self ):
        '''Return the verbose argument'''
        return self.params.get( 'verbose' )

    def archive_dst ( self ):
        '''Return the archive_dst argument'''
        return self.params.get( 'archive_dst' )


    def skip_complete( self ):
        '''Return the skip_complete argument'''
        return self.params.get( 'skip_complete' )

    def roon_dst ( self ):
        '''Return the roon_dst argument'''
        return self.params.get( 'roon_dst' )

    def extract_dst ( self ):
        '''Return the extract_dst argument'''
        return self.params.get( 'extract_dst' )

    def roon_target ( self ):
        '''Return the roon_target argument'''
        return self.params.get( 'roon_target' )

class FileBase:
    '''The base clase for Album and FlacFile'''
    def __init__( self, config ):
        self.config = config

    def sanitize_text( self, txt, charset ):
        '''Change the text to conform with what is expected'''
        for replacement in self.config[ 'Cleanup' ][ charset ]:
            dst = replacement[ "dst"]
            for src in replacement[ "src" ]:
                txt = txt.replace( src, dst )
        # Removing leading and tailing whitespaces
        txt = txt.strip()
        # FIXME: skip Roman numbers
        # FIXME: capwords is not good
        #return string.capwords( txt )
        return txt

    def sanitize_text_display( self, txt ):
        '''Change the text to display on screen'''
        return self.sanitize_text( txt, 'Display Chars' )

    def sanitize_text_filesystem( self, txt ):
        '''Change the text for a filename'''
        return self.sanitize_text( txt, 'Filesystem Chars' )

    def sanitize_number( self, txt ):
        '''
        Clean up the number tag.
        1) If the number in the format of <num> / <total_num>, retain only <num>
        2) Convet from the string <num> to integer
        '''
        if '/' in txt:
            txt = txt.split( '/' )
            return int( txt[ 0 ] )
        return int( txt )

class Album( FileBase ):
    '''The class representing a folder containing an album'''
    def __init__( self, config, path ):
        super().__init__( config )
        self.path = path
        self.disc = defaultdict( list )
        self.contents = []
        self.track_map = {}

    def not_found_in_roon_library( self ):
        '''Check if this album already exists in the Roon library'''
        if not self.album_artist() or not self.album_name():
            return False

        roon_library = self.config[ 'Roon Library' ][ 'Location']
        roon_target = self.config[ 'Roon Library' ][ 'Default Target' ]
        folder = f'{self.album_artist()} - {self.album_name()}'
        if self.album_artist() == 'Various Artists':
            roon_path = os.path.join( roon_library, roon_target,
                                      self.album_artist(), folder )
        else:
            subdir = folder[ 0 ]
            roon_path = os.path.join( roon_library, roon_target, subdir,
                                      self.album_artist(), folder )
        return not os.path.exists( roon_path )

    def add_track( self, flac ):
        '''Add a track to the album'''
        self.contents.append( flac )
        if flac.discno:
            self.disc[ flac.discno ].append( flac )
            self.track_map[ ( flac.discno, flac.track ) ] = flac
        else:
            self.track_map[ ( 1, flac.track ) ] = flac

    def get_track( self, disc_and_track ):
        '''Get the flac file with this ( disc, track ) number'''
        return self.track_map.get( disc_and_track )

    def get_album_artist_from_path( self ):
        '''
        Get the album artist from the folder name.
        Assuming the folder name is in the format of <Album Artist> - <Album>
        '''
        obj = re.match( r'(.*?) - (.*)', str( self.path.name ) )
        if obj:
            return obj.group( 1 )
        return None

    def get_album_name_from_path( self ):
        '''
        Get the album name from the folder name.
        Assuming the folder name is in the format of <Album Artist> - <Album>
        '''
        obj = re.match( r'(.*?) - (.*)', str( self.path.name ) )
        if obj:
            return obj.group( 2 )
        return None

    def album_name( self ):
        '''
        Return the album name.
        1) If all flac files in this album has the same album name and
           that album name is not empty, use that one.
        2) If there are more than one album name, use the longest common
           string in the album names.
        3) Try to get the album name from the folder name
        '''
        result = list( set( f.album for f in self.contents ) )
        if len( result ) == 1:
            if result[ 0 ] is not None:
                return result[ 0 ]
            return self.get_album_name_from_path()

        name = self.get_album_name_from_path()
        if name:
            return name

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
            return result[ 0 ][ : stop ]
        return None

    def album_artist( self ):
        '''
        Return the album artist.
        1) If all flac files in this album has the same album name and
           that album name is not empty, use that one.
        2) Try to get the album name from the folder name
        '''
        result = list( set( f.album_artist for f in self.contents ) )
        # All flac files in this album should have the same album artist
        # But sometimes mistake happens.
        if len( result ) == 1 and result[ 0 ]:
            return result[ 0 ]
        return self.get_album_artist_from_path()

    def has_all_tags( self ):
        '''Check if all flac files have all the required tags'''
        check_discno = bool( self.disc )
        return all( f.has_all_tags( check_discno=check_discno )
                    for f in self.contents )

    def has_album_art( self ):
        '''Check if all flac files have an album art'''
        return all( f.has_album_art for f in self.contents )

    def get_format( self, filename ):
        '''Determine the file format from the filename'''
        filename = str( filename.name )
        return os.path.splitext( filename )[ -1 ].lower()

    def get_unwanted_files( self ):
        '''Get the list of unwanted files'''
        unwanted = []
        filenames = [ f for f in self.path.glob( '**/*' ) if os.path.isfile( f ) ]
        for filename in filenames:
            fmt = self.get_format( filename )
            if fmt not in self.config[ "Cleanup" ][ "Allowed Formats" ]:
                unwanted.append( filename )
        return unwanted

    def no_unwanted_files( self ):
        '''Check if this album contains unwanted files'''
        return not bool( self.get_unwanted_files() )

    def remove_unwanted_files( self ):
        '''Remove files of which format is not in the allowed list'''
        deletes = self.get_unwanted_files()
        if not deletes:
            return

        for filename in deletes:
            print( f'Removing {filename}' )
        confirm = input( 'Are you sure? [y] ' )
        print()
        if confirm != 'y':
            return

        # Remove unwanted files
        for filename in deletes:
            os.remove( filename )
        # Remove empty folders
        folders = [ str( f ) for f in self.path.glob( '**/*' )
                    if os.path.isdir( f ) ]
        for folder in sorted( folders, key=len, reverse=True ):
            if not list( os.listdir( folder ) ):
                os.rmdir( folder )

    def save( self ):
        '''Save all tag changes to disck'''
        album_name = self.album_name()
        album_artist = self.album_artist()
        if self.disc:
            for disc, flacs in self.disc.items():
                for flac in flacs:
                    flac.album = album_name
                    flac.album_artist = album_artist
                    flac.discno = disc
                    flac.save()
        else:
            for flac in self.contents:
                flac.album = album_name
                flac.album_artist = album_artist
                flac.save()

    def rename( self ):
        '''Rename all the files in the folder and this folder'''
        for flac in self.contents:
            flac.rename()

        # Rename this folder
        parent = str( self.path.parent )
        album_artist = self.sanitize_text_filesystem( self.album_artist() )
        album_name = self.sanitize_text_filesystem( self.album_name() )
        dst = os.path.join( parent, f'{album_artist} - {album_name}' )
        if str( self.path ) == dst:
            return
        os.rename( str( self.path ), dst )

        # Re-add all files in this folders
        self.path = Path( dst )
        self.disc = defaultdict( list )
        self.contents = []
        self.track_map = {}
        for filename in self.path.glob( '**/*.flac' ):
            self.add_track( FlacFile( self.config, filename ) )

    def ready_to_copy( self ):
        '''This album is ready to be copied to the Roon library'''
        return all( [ self.has_all_tags(),
                      self.has_album_art(),
                      self.no_unwanted_files(),
                      self.not_found_in_roon_library()  ])

    def show_content( self ):
        '''Show the contents of this album'''
        print( f'Album Artist : {self.album_artist()}' )
        print( f'Album : {self.album_name()}' )
        #print( f'Album Art: {self.has_album_art()}' )

        warning = ''
        if not self.no_unwanted_files():
            warning += '"Unwanted files are found."'
        if not self.not_found_in_roon_library():
            warning = warning + ', ' if warning else warning
            warning += '"Found in Roon"'
        if warning:
            print( f'Warning : {warning}' )
        # print( f'No Unwanted Files : {self.no_unwanted_files()}' )
        # print( f'Not found in Roon library : {self.not_found_in_roon_library()}' )

        if len( self.disc ) > 1:
            for disc, flacs in self.disc.items():
                print( f'Disc {disc}' )
                tab_data = []
                for flac in sorted( flacs, key=lambda x: x.track ):
                    track = flac.track if flac.track else 'None'
                    artist = flac.artist if flac.artist else 'None'
                    title = flac.title if flac.title else 'None'
                    tab_data.append( [ track, artist, title, str( flac.path.name ) ] )
                print( tabulate( tab_data, tablefmt="plain" ) )
        else:
            tab_data = []
            for flac in sorted( self.contents, key=lambda x: x.track ):
                track = flac.track if flac.track else 'None'
                artist = flac.artist if flac.artist else 'None'
                title = flac.title if flac.title else 'None'
                tab_data.append( [ track, artist, title, str( flac.path.name ) ] )
            print( tabulate( tab_data, tablefmt="plain" ) )

# pylint: disable=too-many-instance-attributes
class FlacFile( FileBase ):
    '''The class representing a flac file'''
    def __init__( self, config, path ):
        super().__init__( config )
        self.path = path
        self.metadata = None
        self.track = None
        self.title = None
        self.artist = None
        self.album = None
        self.album_artist = None
        self.discno = None
        self.has_album_art = None
        self.load_metadata()

    def load_metadata( self ):
        '''Load the metadata from the disk'''
        self.metadata = FLAC( self.path )
        self.track = self.get_track_number()
        self.title = self.get_title()
        self.artist = self.get_metadata_str( 'artist' )
        self.album = self.get_metadata_str( 'album' )
        self.album_artist = self.get_metadata_str( 'albumartist' )
        self.discno = self.get_disc_number()
        self.has_album_art = self.check_album_art()

    def rename( self ):
        '''Rename this file to <track> <title>.flac'''
        parent = str( self.path.parent )
        # It is unlikely that there will be more than 99 tracks in an album.
        filename = f'{self.track:02} {self.title}.flac'
        filename = self.sanitize_text_filesystem( filename )
        dst = os.path.join( parent, filename )
        if str( self.path ) == dst:
            return
        os.rename( str( self.path ), dst )
        self.path = Path( dst )
        self.load_metadata()

    def get_metadata( self, field ):
        '''Get a tag'''
        title = self.metadata.get( field )
        return title[ 0 ] if title else None

    def get_metadata_num( self, field ):
        '''Get a sanitized numeric tag'''
        result = self.get_metadata( field )
        return self.sanitize_number( result ) if result else None

    def get_metadata_str( self, field ):
        '''Get a sanitized string tag'''
        result = self.get_metadata( field )
        return self.sanitize_text_display( result ) if result else None

    def get_track_number( self ):
        '''
        Get the track number from ID3 tag first.
        If that fails, then the filename
        '''
        track = self.get_metadata_num( 'tracknumber' )
        if track:
            return track

        filename = self.sanitize_text_display( str( self.path.name ) )
        obj = re.match( r'^(\d+) *(.*)', filename )
        if obj:
            return obj.group( 1 )
        return None

    def get_title( self ):
        '''Get the title from ID3 tag first.  If that fails, then the filename'''
        title = self.get_metadata_str( 'title' )
        if title:
            return title

        filename = self.sanitize_text_display( str( self.path.name ) )
        obj = re.match( r'^(\d+) *(.*)', filename )
        if obj:
            return obj.group( 2 )
        return None

    def get_disc_number_from_metadata( self ):
        '''Retrieve the disc number from the metadata in the file'''
        discno = self.get_metadata_num( 'discnumber' )
        return discno if discno else None

    def get_disc_number_from_path( self ):
        '''Retrieve the disc number from the file path'''
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
        '''
        Get the disc number of this file. For Disc No,
        we trust the information from the path first.
        '''
        discno = self.get_disc_number_from_path()
        if not discno:
            discno = self.get_disc_number_from_metadata()
        return discno

    def check_album_art( self ):
        '''Check if this file contains an album art'''
        metadata = FLAC( self.path )
        for pic in metadata.pictures:
            if pic.type == 3:
                return True
        return False

    def has_all_tags( self, check_discno=False):
        '''Check if this file has all required tags'''
        if not check_discno:
            return all( [ self.track, self.title, self.artist, self.album,
                          self.album_artist ] )
        return all( [ self.track, self.title, self.artist, self.album,
                      self.album_artist, self.discno ] )

    def album_path( self ):
        '''Get the path containing this album'''
        parent = self.path.absolute().parent
        if re.search( r'cd.*(\d+)', str( parent ).lower() ) or \
                re.search( r'disc.*(\d+)', str( parent ).lower() ):
            parent = parent.parent
        return parent

    def save( self ):
        '''Save all ID3 tag changes to disk'''
        for key in self.metadata.keys():
            del self.metadata[ key ]
        self.metadata[ 'tracknumber' ] = [ str( self.track ) ]
        self.metadata[ 'title' ] = [ self.title ]
        self.metadata[ 'artist' ] = [ self.artist ]
        self.metadata[ 'album' ] = [ self.album ]
        self.metadata[ 'albumartist' ] = [ self.album_artist ]
        if self.discno:
            self.metadata[ 'discnumber' ] = [ str( self.discno ) ]
        self.metadata.save()

    def dump_metadata( self ):
        '''Dump all ID3 tags'''
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
        self.archive_dst = params.archive_dst()
        self.extract_dst = params.extract_dst()
        self.verbose = params.verbose()
        self.dry_run = params.dry_run()

    def __str__( self ):
        return f'Extracting {self.filename}'

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
        self.verbose = params.verbose()
        self.dry_run = params.dry_run()

        self.format = self.get_format()
        self.tags = self.get_tags()
        self.album_art = self.get_album_art()

    def __str__( self ):
        return f'Converting {self.filename}'

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
        metadata = None
        if self.format == 'wav':
            metadata = WAVE( self.filename )
        else:
            raise UnsupportedFormat( self.filename )

        if not metadata:
            return None

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
        self.verbose = params.verbose()
        self.dry_run = params.dry_run()
        self.roon_dst = params.roon_dst()
        self.skip_complete = params.skip_complete()
        self.albums = {}

    def load_flac_files( self ):
        '''Load all flac files'''
        cwd = Path( self.location )
        filenames = [ f for f in cwd.glob( '**/*.flac' )
                      if self.roon_dst and \
                              self.roon_dst not in str( f.absolute() ) ]
        for filename in filenames:
            flac = FlacFile( self.config, filename )
            if flac.album_path() not in self.albums:
                self.albums[ flac.album_path() ] = \
                        Album( self.config, flac.album_path() )
            self.albums[ flac.album_path() ].add_track( flac )

    def command_prompt( self ):
        '''Temporary interactive command'''
        for album in self.albums.values():
            if self.skip_complete and album.ready_to_copy():
                continue

            album.show_content()
            print()
            cmd = input( 'Enter command[q/c/sa/sh/cp/fi/fo/album/artist/tt/ta/dtt/dta/tre/are]: ' )
            while True:
                show = False
                if cmd in [ 'q', 'quit' ]:
                    return
                if cmd in [ 'c', 'cont' ]:
                    break
                if cmd in [ 'sa', 'save' ]:
                    album.save()
                    album.remove_unwanted_files()
                    album.rename()
                    show = True
                elif cmd in [ 'sh', 'show' ]:
                    show = True
                elif cmd in [ 'cp', 'copy' ]:
                    # copy album artist to each file
                    for flac in album.contents:
                        flac.artist = album.album_artist()
                    show = True
                elif cmd in [ 'fo', 'folder' ]:
                    # copy album artist and album from album folder
                    album_artist = album.get_album_artist_from_path()
                    album_name = album.get_album_name_from_path()
                    for flac in album.contents:
                        flac.album_artist = album_artist
                        flac.album = album_name
                    show = True
                elif cmd in [ 'fi', 'file' ]:
                    for flac in album.contents:
                        flac.title = str( flac.path.name )
                    show = True
                elif cmd.startswith( 'album '):
                    # Change the album name
                    # ab <album>
                    album_name = cmd[ len( 'album ' ): ]
                    for flac in album.contents:
                        flac.album = album_name
                    show = True
                elif cmd.startswith( 'artist '):
                    # Change the album artist
                    # at <album artist>
                    album_artist = cmd[ len( 'artist ' ): ]
                    for flac in album.contents:
                        flac.album_artist = album_artist
                    show = True
                elif cmd.startswith( 'tt' ):
                    # Change the track titile
                    # tt <track> <title>
                    obj = re.match( r'^tt (\d+) (.*)$', cmd )
                    if obj:
                        track = int( obj.group( 1 ) )
                        title = obj.group( 2 )
                        flac = album.get_track( ( 1, track ) )
                        flac.title = title
                        show = True
                elif cmd.startswith( 'ta'):
                    # Change the track artist
                    # ta <track> <title>
                    obj = re.match( r'^ta (\d+) (.*)$', cmd )
                    if obj:
                        track = int( obj.group( 1 ) )
                        artist = obj.group( 2 )
                        flac = album.get_track( ( 1, track ) )
                        flac.artist = artist
                        show = True
                elif cmd.startswith( 'dtt'):
                    # Change ( disc, track ) title
                    # dtt <disc> <trac> <title>
                    obj = re.match( r'^dtt (\d+) (\d+) (.*)$', cmd )
                    if obj:
                        disc = int( obj.group( 1 ) )
                        track = int( obj.group( 2 ) )
                        title = obj.group( 3 )
                        flac = album.get_track( ( disc, track ) )
                        flac.title = title
                        show = True
                elif cmd.startswith( 'dta'):
                    # Change ( disc, track ) artist
                    # dta <disc> <trac> <title>
                    obj = re.match( r'^dta (\d+) (\d+) (.*)$', cmd )
                    if obj:
                        disc = int( obj.group( 1 ) )
                        track = int( obj.group( 2 ) )
                        artist = obj.group( 3 )
                        flac = album.get_track( ( disc, track ) )
                        flac.artist = artist
                        show = True
                elif cmd.startswith( 'tre' ):
                    # re <regular expression>
                    regex = cmd[ len( 'tre ' ): ]
                    print( regex )
                    for flac in album.contents:
                        obj = re.match( regex, flac.title )
                        if obj:
                            show = True
                            flac.title = obj.group( 1 )
                elif cmd.startswith( 'are' ):
                    # re <regular expression>
                    regex = cmd[ len( 'are ' ): ]
                    for flac in album.contents:
                        obj = re.match( regex, flac.artist )
                        if obj:
                            show = True
                            flac.artist = obj.group( 1 )
                if show:
                    album.show_content()


                cmd = input( 'Enter command[q/c/sa/sh/cp/fi/fo/album/artist/tt/ta/dtt/dta/tre/are]: ' )
                print()

    def show_summary( self ):
        '''Show the summary of all albums'''
        complete_albums = []
        incomplete_albums = []
        for album in self.albums.values():
            album_artist = album.album_artist()
            album_name = album.album_name()

            if album.ready_to_copy():
                complete_albums.append( [ album_artist, album_name ] )
            else:
                incomplete_albums.append( [ album_artist, album_name,
                                            album.has_all_tags(),
                                            album.has_album_art(),
                                            album.no_unwanted_files(),
                                            album.not_found_in_roon_library() ] )

        complete_header = [ 'Album Artist', 'Album' ]
        print( tabulate( complete_albums, headers=complete_header ) )
        print()

        if not incomplete_albums:
            return
        tab_header = [ 'Album Artist', 'Album', 'Has All Tags', 'Has Album Art',
                       'No Unwanted Files', 'Not Found in Roon' ]
        print( tabulate( incomplete_albums, headers=tab_header ) )
        print()

    def run( self ):
        '''Run the command'''
        self.load_flac_files()
        self.show_summary()
        self.command_prompt()
        self.show_summary()

class RoonCopyCmd( CleanupCmd ):
    '''The command to copy complete albums to Roon library'''
    def __init__( self, location, config, params ):
        super().__init__( location, config, params )
        self.roon_dst = params.roon_dst()
        self.roon_target = params.roon_target()

    def roon_copy( self ):
        '''Copy all complete albums to Roon library'''
        copy_albums = [ a for a in self.albums.values() if a.ready_to_copy() ]
        if not self.dry_run and copy_albums:
            os.makedirs( self.roon_dst, exist_ok=True )

        for album in copy_albums:
            album_path = str( album.path.name )
            cmd = f'rooncpy -t {self.roon_target} "{album_path}"'
            try:
                if self.verbose:
                    print( cmd )
                if not self.dry_run:
                    subprocess.check_output( cmd, shell=True, text=True )

                if self.verbose:
                    print( f'shutil.move( {album.path.absolute()}, {self.roon_dst} )' )
                if not self.dry_run:
                    shutil.move( album.path.absolute(), self.roon_dst )
            except subprocess.CalledProcessError as exception:
                print( exception )

    def run( self ):
        self.load_flac_files()
        self.roon_copy()

def execute( cmd ):
    '''Execute a command'''
    cmd.run()

class AudioTag:
    '''The main class for our Audio file tagging program'''
    def __init__( self, config ):
        self.config = config

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
            for cmd in cmds:
                cmd.verbose = False
            print( *( cmd for cmd in cmds ), sep='\n' )
            with ProcessPoolExecutor( max_workers=cpu_count ) as executor:
                tasks = [ executor.submit( func, c ) for c in cmds]
                for _ in progress_bar( concurrent.futures.as_completed( tasks ), total=size ):
                    pass

    def extract_archives( self, params ):
        '''Extract all archives'''
        cwd = Path( os.getcwd() )
        cmds = []
        for fmt in self.config[ "Extract" ][ "Archive Format" ]:
            cmds += [ ExtractCmd( f, params ) for f in cwd.glob( f'**/*{fmt}' )
                      if params.archive_dst() and \
                              params.archive_dst() not in str( f.absolute() ) ]
        if cmds and not params.dry_run():
            os.makedirs( params.archive_dst(), exist_ok=True )
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec() )

    def convert_audio( self, params ):
        '''Convert the autio files to .flac'''
        cwd = Path( os.getcwd() )
        cmds = []
        for fmt in self.config[ "Extract" ][ "Convert Format" ]:
            cmds += [ ConvertCmd( f, params ) for f in cwd.glob( f'**/*{fmt}' ) ]
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec() )

    def cleanup( self, params ):
        '''Do various data cleanup on all folders in the current folder'''
        cmds = [ CleanupCmd( os.getcwd(), self.config, params ) ]
        self.execute_commands( execute, cmds )

    def roon_copy( self, params ):
        '''Do various data cleanup on all folders in the current folder'''
        cmds = [ RoonCopyCmd( os.getcwd(), self.config, params ) ]
        self.execute_commands( execute, cmds )

    def run( self, params ):
        '''Run the autio tag process'''
        if params.command() == 'extract':
            self.extract_archives( params )
        elif params.command() == 'convert':
            self.convert_audio( params )
        elif params.command() == 'cleanup':
            self.cleanup( params )
        elif params.command() == 'copy':
            self.roon_copy( params )
        else:
            raise UnsupportedCommand( params.command() )

def process_arguments( config ):
    '''Process commandline arguments'''
    archive_dst = config[ 'Default Folders' ][ 'Archive' ]
    extract_dst = config[ 'Default Folders' ][ 'Extract' ]
    roon_dst = config[ 'Default Folders' ][ 'Roon' ]
    roon_target = config[ 'Roon Library' ][ 'Default Target' ]

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
    extract_parser.add_argument( '-a', '--archive-dst', default=archive_dst,
                                 help='Move the uncompressed archives to this location' )
    extract_parser.add_argument( '-e', '--extract-dst', default=extract_dst,
                                 help='Extract the archives at this location' )

    subparser.add_parser( 'convert', help='Convert audio files to .flac' )

    cleanup_parser = subparser.add_parser( 'cleanup', help='Do various data cleanup' )
    cleanup_parser.add_argument( '-k', '--skip-complete', action='store_true',
                                 help='Skip the cleaned album' )

    copy_parser = subparser.add_parser( 'copy', help='Copy complete albums to Roon library' )
    copy_parser.add_argument( '-r', '--roon-dst', default=roon_dst,
                              help="Move the copied albums to this location" )
    copy_parser.add_argument( '-t', '--roon-target', action='store',
                              dest='roon_target', default=roon_target,
                              choices=[ 'cd', 'dsd', 'flac', 'mqa' ],
                              help="Move the copied albums to this location" )

    args = parser.parse_args()
    params_dict = {
        "command" : args.command,
        "dry_run" : args.dry_run,
        "verbose" : args.verbose,
        "seq_exec" : False if args.command in [ 'cleanup', 'copy' ] \
                     else args.seq_exec,
        "skip_complete" : getattr( args, 'skip_complete', False ),
        "archive_dst" : getattr( args, 'archive_dst', archive_dst ),
        "extract_dst" : getattr( args, 'extract_dst', extract_dst ),
        "roon_dst" : getattr( args, 'roon_dst', roon_dst ),
        "roon_target" : getattr( args, 'roon_target', roon_target ),
    }
    return Parameters( params_dict )

def main():
    '''The main function'''
    config = load_config( CONFIG_FILENAME )
    params = process_arguments( config )
    audiotag = AudioTag( config )
    audiotag.run( params )

if __name__ == '__main__':
    main()
