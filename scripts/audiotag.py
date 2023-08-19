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
# pylint: disable=unused-import
# readline will change the behavior of input() even though it is not called
import readline
import shutil

# pylint: disable=import-error
from fastprogress import progress_bar
from mutagen.flac import FLAC, Picture
from mutagen.dsf import DSF
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TPE2, TPOS, PictureType
from mutagen.wave import WAVE
from pydub import AudioSegment
from pydub.utils import mediainfo
from tabulate import tabulate
import mutagen
import pyunpack

from genutils import load_config, RomanNumeric

CONFIG_FILENAME = "config/audiotag.json"

class UnsupportedFormat( Exception ):
    '''Unsupport Audio Format'''

class UnsupportedCommand( Exception ):
    '''Unsupport Command'''

class UnimplementedMethod( Exception ):
    '''Unimplemented Method'''

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

    def skip_complete( self ):
        '''Return the skip_complete argument'''
        return self.params.get( 'skip_complete' )

    def flac_target ( self ):
        '''Return the flac_target argument'''
        return self.params.get( 'flac_target' )

class TextSanitizer:
    '''The base clase for Album and AudioFile'''
    def __init__( self, config ):
        self.config = config

    def sanitize_text( self, txt, charset, capitalize=False ):
        '''Change the text to conform with what is expected'''
        for replacement in self.config[ 'Cleanup' ][ charset ]:
            dst = replacement[ "dst"]
            for src in replacement[ "src" ]:
                txt = txt.replace( src, dst )
        # Removing leading and tailing whitespaces
        txt = txt.strip()

        if not capitalize:
            return txt

        new_txt = []
        for token in txt.split():
            token = token.lower()
            if len( token ) == 1 or \
                    token.lower() == 'ost' or \
                    RomanNumeric().is_valid( token ):
                token = token.upper()
            elif token[ -1 ] in [ '.' ] and RomanNumeric().is_valid( token[ :-1] ):
                # For matching 'I.' found frequently in classical music titles
                token = token[ :-1 ].upper() + token[ -1 ]
            elif token[ 0 ] in [ '(', '[', '{' ]:
                # Capitalize the next word character if (, [, or { is present
                i = 1
                while i < len( token) and ( ord( token[ i ] ) < ord( 'a' ) or \
                                            ord( token[ i ] ) > ord( 'z' ) ):
                    i += 1
                if i < len( token ):
                    token = token[ : i ] + token[ i ].upper() + token[ i + 1: ]
            else:
                # Capitalize the first character only
                token = token[ 0 ].upper() + token[ 1: ]
            new_txt.append( token )
        return ' '.join( new_txt )

    def sanitize_text_display( self, txt, capitalize=False ):
        '''Change the text to display on screen'''
        return self.sanitize_text( txt, 'Display Chars', capitalize=capitalize )

    def sanitize_text_filesystem( self, txt, capitalize=False ):
        '''Change the text for a filename'''
        return self.sanitize_text( txt, 'Filesystem Chars', capitalize=capitalize )

    def sanitize_number( self, txt ):
        '''
        Clean up the number tag.
        1) If the number in the format of <num> / <total_num>, retain only <num>
        2) Convet from the string <num> to integer
        '''
        txt = txt.split( '/' )[ 0 ] if '/' in txt else txt
        try:
            num = int( txt )
        except ValueError as exception:
            print( exception )
            num = None
        return num

class Album( TextSanitizer ):
    '''The class representing a folder containing an album'''
    def __init__( self, config, path ):
        super().__init__( config )
        self.path = path
        self.disc = defaultdict( list )
        self.contents = []
        self.track_map = {}

    def not_found_in_roon_library( self, target=None ):
        '''Check if this album already exists in the Roon library'''
        if not self.album_artist() or not self.album_name():
            return True

        roon_config = self.config[ 'Roon Library' ]
        roon_library = roon_config[ 'Location']
        target = target if target else roon_config[ 'Default Target' ]
        folder = f'{self.album_artist()} - {self.album_name()}'
        if self.album_artist() == 'Various Artists':
            roon_path = os.path.join( roon_library, target,
                                      self.album_artist(), folder )
        else:
            subdir = folder[ 0 ]
            roon_path = os.path.join( roon_library, target, subdir,
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
        result = list( set( f.album for f in self.contents if f.album is not None ) )
        if not result:
            return None
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
        confirm = input( 'Are you sure? [Y/n] ' )
        print()
        if confirm not in ( '', 'y', 'Y' ):
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

    def refresh( self ):
        '''Re-add all files in this folders'''
        self.disc = defaultdict( list )
        self.contents = []
        self.track_map = {}
        for ext in self.config[ 'Cleanup' ][ 'Supported Formats' ]:
            for filename in self.path.glob( f'**/*{ext}' ):
                self.add_track( AudioFile( self.config, filename ) )

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
        self.path = Path( dst )
        self.refresh()

    def ready_to_copy( self, target=None ):
        '''This album is ready to be copied to the Roon library'''
        return all( [ self.has_all_tags(),
                      self.has_album_art(),
                      self.no_unwanted_files(),
                      self.not_found_in_roon_library( target=target )  ])

    def show_content( self ):
        '''Show the contents of this album'''
        print()
        print( f'Folder : {self.path.name}' )
        print( f'Album Artist : {self.album_artist()}' )
        print( f'Album : {self.album_name()}' )

        warning = '"Unwanted files are found."' if not self.no_unwanted_files() else ''
        if not self.not_found_in_roon_library():
            msg = '"Found in Roon"'
            warning = warning + ', ' + msg if warning else msg
        if not self.has_all_tags():
            msg = '"Missing required tags"'
            warning = warning + ', ' + msg if warning else msg
        if not self.has_album_art():
            msg = '"Missing album art"'
            warning = warning + ', ' + msg if warning else msg
        if warning:
            print( f'Warning : {warning}' )
        print( f'Ready to copy : {self.ready_to_copy()}' )

        headers = [ 'Track', 'Artist', 'Title', 'Cover', 'Filename' ]
        if len( self.disc ) > 1:
            for disc, flacs in self.disc.items():
                disc_folder_found = False
                for disc_folder in [ 'CD', 'Disc ' ]:
                    disc_folder += str( disc )
                    disc_folder = \
                            os.path.join( self.path.absolute(), disc_folder )
                    if os.path.exists( disc_folder ):
                        disc_folder_found = True
                        break
                disc_msg = f'Disc {disc}' if disc_folder_found \
                           else f'Disc {disc} NOT FOUND'
                print( disc_msg )

                tab_data = []
                for flac in sorted( flacs, key=lambda x: int( x.track ) ):
                    track = flac.track if flac.track else 'None'
                    artist = flac.artist if flac.artist else 'None'
                    title = flac.title if flac.title else 'None'
                    tab_data.append( [ track, artist, title, flac.has_album_art,
                                       str( flac.path.name ) ] )
                print( tabulate( tab_data, headers=headers, tablefmt="plain" ) )
        else:
            tab_data = []
            for flac in sorted( self.contents, key=lambda x: x.track ):
                track = flac.track if flac.track else 'None'
                artist = flac.artist if flac.artist else 'None'
                title = flac.title if flac.title else 'None'
                tab_data.append( [ track, artist, title, flac.has_album_art,
                                   str( flac.path.name ) ] )
            print( tabulate( tab_data, headers=headers, tablefmt="plain" ) )

class MetadataBase( TextSanitizer ):
    '''Base class for metadata'''
    def __init__( self, config, path ):
        super().__init__( config )
        self.path = path
        self.metadata = None

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

    def get_track( self ):
        '''Get the track number of the song'''
        raise UnimplementedMethod

    def get_title( self ):
        '''Get the title of the song'''
        raise UnimplementedMethod

    def get_artist( self ):
        '''Get the artist of the song'''
        raise UnimplementedMethod

    def get_album( self ):
        '''Get the album of the song'''
        raise UnimplementedMethod

    def get_album_artist( self ):
        '''Get the album artist of the song'''
        raise UnimplementedMethod

    def get_disc( self ):
        '''Get the disc number of the song'''
        raise UnimplementedMethod

    def has_album_art( self ):
        '''Check if the file contains an album art'''
        raise UnimplementedMethod

    def dump_metadata( self ):
        '''Dump all ID3 tags'''
        for tag, value in self.metadata.items():
            print( f'{tag} = {value}' )

class MetadataFlac( MetadataBase ):
    '''Metadata class for .flac files'''
    def __init__( self, config, path ):
        super().__init__( config, path )
        self.metadata = FLAC( self.path )

    def get_track( self ):
        return self.get_metadata_num( 'tracknumber' )

    def get_title( self ):
        return self.get_metadata_str( 'title' )

    def get_artist( self ):
        return self.get_metadata_str( 'artist' )

    def get_album( self ):
        return self.get_metadata_str( 'album' )

    def get_album_artist( self ):
        return self.get_metadata_str( 'albumartist' )

    def get_disc( self ):
        return self.get_metadata_num( 'discnumber' )

    def has_album_art( self ):
        '''Check if this file contains an album art'''
        for pic in self.metadata.pictures:
            if pic.type == 3:
                return True
        return False

    def save( self, new_metadata ):
        '''Write the new metadata to disk'''
        for key in self.metadata.keys():
            del self.metadata[ key ]
        for key, value in new_metadata.items():
            if not value:
                continue
            self.metadata[ key ] = [ value ]
        self.metadata.save()

class MetadataID3( MetadataBase ):
    '''Common metadata class for audio files that use ID3'''
    def __init__( self, config, path ):
        super().__init__( config, path )
        if  self.path.suffix == '.dsf':
            self.metadata = DSF( self.path )
        else:
            assert False, "Unsupported Format"

    def get_track( self ):
        return self.get_metadata_num( 'TRCK' )

    def get_title( self ):
        return self.get_metadata_str( 'TIT2' )

    def get_artist( self ):
        return self.get_metadata_str( 'TPE1' )

    def get_album( self ):
        return self.get_metadata_str( 'TALB' )

    def get_album_artist( self ):
        return self.get_metadata_str( 'TPE2' )

    def get_disc( self ):
        return self.get_metadata_num( 'TPOS' )

    def has_album_art( self ):
        return 'APIC:Picture' in self.metadata

    def save( self, new_metadata ):
        '''Write the new metadata to disk'''
        self.metadata[ 'TRCK' ] = TRCK( encoding=3, text=new_metadata[ 'tracknumber' ] )
        self.metadata[ 'TIT2' ] = TIT2( encoding=3, text=new_metadata[ 'title' ] )
        self.metadata[ 'TPE1' ] = TPE1( encoding=3, text=new_metadata[ 'artist' ] )
        self.metadata[ 'TALB' ] = TALB( encoding=3, text=new_metadata[ 'album' ] )
        self.metadata[ 'TPE2' ] = TPE2( encoding=3, text=new_metadata[ 'albumartist' ] )
        if 'disc' in new_metadata:
            self.metadata[ 'TPOS' ] = TPOS( encoding=3, text=new_metadata[ 'discnumber' ] )
        self.metadata.save()

# pylint: disable=too-many-instance-attributes
class AudioFile( TextSanitizer ):
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
        self.initialized = False
        self.load_metadata()

    def load_metadata( self ):
        '''Load the metadata from the disk'''
        try:
            if self.path.suffix == '.flac':
                self.metadata = MetadataFlac( self.config, self.path )
            elif self.path.suffix == '.dsf':
                self.metadata = MetadataID3( self.config, self.path )
            else:
                raise UnsupportedFormat( self.path )
        except mutagen.flac.error:
            print( f'Unable to read {self.path.absolute()}' )
            return
        self.track = self.get_track_number()
        self.title = self.get_title()
        self.discno = self.get_disc_number()
        self.artist = self.metadata.get_artist()
        self.album = self.metadata.get_album()
        self.album_artist = self.metadata.get_album_artist()
        self.has_album_art = self.metadata.has_album_art()
        self.initialized = True

    def rename( self ):
        '''Rename this file to <track> <title>.<ext>'''
        parent = str( self.path.parent )
        # It is unlikely that there will be more than 99 tracks in an album.
        filename = f'{self.track:02} {self.title}{self.path.suffix}'
        filename = self.sanitize_text_filesystem( filename )
        dst = os.path.join( parent, filename )
        if str( self.path ) == dst:
            return
        os.rename( str( self.path ), dst )
        self.path = Path( dst )
        self.load_metadata()

    def get_track_number( self ):
        '''
        Get the track number from ID3 tag first.
        If that fails, then the filename
        '''
        track = self.metadata.get_track()
        if track:
            return track

        filename = self.sanitize_text_display( str( self.path.name ) )
        obj = re.match( r'^(\d+) *(.*)', filename )
        if obj:
            return int( obj.group( 1 ) )
        # Track 0 means invalid
        return 0

    def get_title( self ):
        '''Get the title from ID3 tag first.  If that fails, then the filename'''
        title = self.metadata.get_title()
        if title:
            return title

        filename = self.sanitize_text_display( str( self.path.name ) )
        obj = re.match( r'^(\d+) *(.*)', filename )
        if obj:
            return obj.group( 2 )
        return None

    def get_disc_number( self ):
        '''
        Retrieve the disc number from the file path first.
        If failed, try to get it from the metadata
        '''
        discno = None
        parent = self.path.absolute().parent.name
        obj = re.search( r'^cd\D*(\d+)', parent.lower() )
        if obj:
            discno = int( obj.group( 1 ) )
        else:
            obj = re.search( r'^disc\D*(\d+)', parent.lower() )
            if obj:
                discno = int( obj.group( 1 ) )
            else:
                discno = self.metadata.get_disc()
        return discno

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
        new_metadata = {
            'tracknumber' : str( self.track ),
            'title' : self.title,
            'artist' : self.artist,
            'album' : self.album,
            'albumartist' : self.album_artist,
            'discnumber' : str( self.discno ) if self.discno else None,
        }
        self.metadata.save( new_metadata )

    def capitalize( self ):
        '''Capitalize all text fields'''
        self.title = self.sanitize_text_display( self.title, capitalize=True ) \
                if self.title else self.title
        self.artist = self.sanitize_text_display( self.artist, capitalize=True ) \
                if self.artist else self.artist
        self.album = self.sanitize_text_display( self.album, capitalize=True ) \
                if self.album else self.album
        self.album_artist = \
                self.sanitize_text_display( self.album_artist, capitalize=True ) \
                if self.album_artist else self.album_artist

class BaseCmd:
    '''The base class of all commands'''
    def __init__( self, config ):
        self.config = config

    def run( self ):
        '''A virtual function to run the core function of the command'''

    def check_exist( self, filename ):
        '''Check if a file or a folder exists'''
        if not os.path.exists( filename ):
            raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT),
                                     filename )

class ExtractCmd( BaseCmd ):
    '''The command to extract a compressed file'''
    def __init__( self, config, filename, params ):
        super().__init__( config )
        self.filename = filename
        self.archive_dst = self.config[ 'Extract' ][ 'Archive' ]
        self.extract_dst = self.config[ 'Extract' ][ 'Extract' ]
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
    def __init__( self, config, filename, params ):
        super().__init__( config )
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
    def __init__( self, config, location, params ):
        super().__init__( config )
        self.location = location
        self.verbose = params.verbose()
        self.dry_run = params.dry_run()
        self.flac_target = params.flac_target()
        self.finished_albums = self.config[ 'Cleanup' ][ 'Finished Albums' ]
        self.skip_complete = params.skip_complete()
        self.albums = {}

    def load_audio_files( self ):
        '''Load all flac files'''
        cwd = Path( self.location )
        filenames = []
        for ext in self.config[ 'Cleanup' ][ 'Supported Formats' ]:
            filenames += [ f for f in cwd.glob( f'**/*{ext}' )
                          if self.finished_albums and \
                                  self.finished_albums not in str( f.absolute() ) ]
        corrupted = []
        for filename in filenames:
            flac = AudioFile( self.config, filename )
            if not flac.initialized:
                corrupted.append( flac )
                continue
            if flac.album_path() not in self.albums:
                self.albums[ flac.album_path() ] = \
                        Album( self.config, flac.album_path() )
            self.albums[ flac.album_path() ].add_track( flac )

        corrupted = [ f.album_path() for f in corrupted ]
        if not corrupted:
            return
        for path in corrupted:
            if path in self.albums:
                print( f'Skipping corrupted album {path}' )
                del self.albums[ path ]

    def command_prompt( self ):
        '''Temporary interactive command'''
        def cmd_save( album ):
            try:
                if album.album_artist() is None:
                    print( 'Album artist is missing.')
                    return False
                if album.album_name() is None:
                    print( 'Album name is missing.')
                    return False
                del self.albums[ album.path ]
                album.save()
                album.remove_unwanted_files()
                album.rename()
                self.albums[ album.path ] = album
                album.show_content()
            except ( KeyError, ValueError )as exception:
                print( exception )
            return False

        def cmd_delete( album ):
            print( f'Deleting {album.path.absolute()}' )
            confirm = input( 'Are you sure? [Y/n] ' )
            if confirm in ( '', 'y', 'Y' ):
                shutil.rmtree( str( album.path.absolute() ) )
            print()
            return True

        def cmd_refresh( album ):
            album.refresh()
            album.show_content()
            return False

        def cmd_copy_album_artist_to_artist( album ):
            for flac in album.contents:
                flac.artist = album.album_artist()
            album.show_content()
            return False

        def cmd_copy_folder_to_album_name_artist( album ):
            album_artist = album.get_album_artist_from_path()
            album_name = album.get_album_name_from_path()
            for flac in album.contents:
                flac.album_artist = album_artist
                flac.album = album_name
            album.show_content()
            return False

        def cmd_copy_filename_to_title( album ):
            for flac in album.contents:
                flac.title = str( flac.path.name )
            album.show_content()
            return False

        def cmd_set_album( album, cmd ):
            # album <album name>
            # artist <album artist>
            for flac in album.contents:
                if cmd.startswith( 'album ' ):
                    flac.album = cmd[ len( 'album ' ): ]
                elif cmd.startswith( 'ab' ):
                    flac.album = cmd[ len( 'ab ' ): ]
                elif cmd.startswith( 'artist ' ):
                    flac.album_artist = cmd[ len( 'artist ' ): ]
                elif cmd == 'atva':
                    flac.album_artist = 'Various Artists'
                elif cmd.startswith( 'at' ):
                    flac.album_artist = cmd[ len( 'at ' ): ]
            album.show_content()
            return False

        def cmd_set_track( album, cmd ):
            # Change the track artist or title
            # ta <track> <title>
            # tt <track> <title>
            obj = re.match( r'^t[a|t] (\d+) (.*)$', cmd )
            if obj:
                track = int( obj.group( 1 ) )
                field = obj.group( 2 )
                flac = album.get_track( ( 1, track ) )
                if cmd.startswith( 'tt' ):
                    flac.title = field
                elif cmd.startswith( 'ta ' ):
                    flac.artist = field
                album.show_content()
            return False

        def cmd_set_disc_track( album, cmd ):
            # Change ( disc, track ) artist or title
            # dta <disc> <trac> <title>
            # dtt <disc> <trac> <title>
            obj = re.match( r'^dt[a|t] (\d+) (\d+) (.*)$', cmd )
            if obj:
                disc = int( obj.group( 1 ) )
                track = int( obj.group( 2 ) )
                field = obj.group( 3 )
                flac = album.get_track( ( disc, track ) )
                if cmd.startswith( 'dta' ):
                    flac.artist = field
                elif cmd.startswith( 'dtt' ):
                    flac.title = field
                album.show_content()
            return False

        def cmd_set_track_regex( album, cmd ):
            # rea <regular expression>
            # ret <regular expression>
            try:
                dirty = False
                if cmd.startswith( 'rea' ):
                    regex = cmd[ len( 'rea ' ): ]
                    for flac in album.contents:
                        obj = re.match( regex, flac.artist )
                        if obj:
                            dirty = True
                            flac.artist = obj.group( 1 )
                elif cmd.startswith( 'ret' ):
                    regex = cmd[ len( 'ret ' ): ]
                    for flac in album.contents:
                        obj = re.match( regex, flac.title )
                        if obj:
                            dirty = True
                            flac.title = obj.group( 1 )
                if dirty:
                    album.show_content()
            except ( IndexError, re.error ) as exception:
                print( exception )
            return False

        def cmd_populate_track_no( album ):
            if len( album.disc ) > 1:
                for _, flacs in album.disc.items():
                    for count, flac in \
                            enumerate( sorted( flacs, key=lambda x: int( x.track ) ) ):
                        flac.track = count + 1
            else:
                for count, flac in \
                        enumerate( sorted( album.contents, key=lambda x: x.track ) ):
                    flac.track = count + 1
            album.show_content()
            return False

        def cmd_continue( album ):
            try:
                error = False
                if cmd in [ 'n', 'next' ]:
                    cmd_save( album )
                    if album.ready_to_copy():
                        os.makedirs( self.finished_albums, exist_ok=True )
                        shutil.move( album.path.absolute(), self.finished_albums )
            except shutil.Error as exception:
                error= True
                print( exception )
            return not error

        def cmd_print( album ):
            print( f'Location: {album.path.absolute()}' )
            return False

        def cmd_capitalize( album ):
            for flac in album.contents:
                flac.capitalize()
            album.show_content()
            return False

        def cmd_help( func_map ):
            tab_data = []
            for keywords, info in func_map[ 'Exact' ].items():
                cmd = ', '.join( list( keywords ) )
                tab_data.append( [ cmd, info[ 'desc' ] ] )
            for keywords, info in func_map[ 'Regex' ].items():
                cmd = ', '.join( list( keywords ) )
                tab_data.append( [ cmd, info[ 'desc' ] ] )
            print( tabulate( tab_data ) )

        def get_input( func_map ):
            keys = [ keywords[ 0 ] for keywords in func_map[ 'Exact' ].keys() ]
            for keywords in func_map[ 'Regex' ].keys():
                keys += list( keywords )
            keys = '/'.join( keys )
            print()
            prompt = f'Enter command[{keys}]: '
            cmd = input( prompt )
            return cmd

        def dispatcher( func_map, cmd, album ):
            for keywords, info in func_map[ 'Exact' ].items():
                if 'func' not in info:
                    continue
                if cmd in keywords:
                    return info[ 'func' ]( album )
            for keywords, info in func_map[ 'Regex' ].items():
                if 'func' not in info:
                    continue
                for k in keywords:
                    if cmd.startswith( k ):
                        return info[ 'func' ]( album, cmd )
            return False

        func_map = {
            "Exact" : {
                ( 'q', 'quit' ) : {
                    'desc' : 'quit',
                },
                ( 'c', 'cont', '' ) : {
                    'desc' : 'continue without saving',
                    'func' : cmd_continue,
                },
                ( 'n', 'next' ) : {
                    'desc' : 'save and continue',
                    'func' : cmd_continue,
                },
                ( 'r', 'refresh' ) : {
                    'desc' : "refresh the content of this album",
                    'func' : cmd_refresh,
                },
                ( 's', 'save' ) : {
                    'desc' : "save changes",
                    'func' : cmd_save,
                },
                ( 'd', 'delete' ) : {
                    'desc' : "delete the album from the filesystem",
                    'func' : cmd_delete,
                },
                ( 'k', 'capitalize' ) : {
                    'desc' : "Capitalize all text fields",
                    'func' : cmd_capitalize,
                },
                ( 'p', 'print' ) : {
                    'desc' : "print the absolute path of the album",
                    'func' : cmd_print,
                },
                ( 'cp', 'copy' ) : {
                    'desc' : 'copy the album artist to the artist in all files',
                    'func' : cmd_copy_album_artist_to_artist,
                },
                ( 'fo', 'folder' ) : {
                    'desc' : 'Use the folder name to imply the album artist and album name',
                    'func' : cmd_copy_folder_to_album_name_artist,
                },
                ( 'fi', 'file' ) : {
                    'desc' : 'Copy the filename to the title of all files',
                    'func' : cmd_copy_filename_to_title
                },
                ( 'tr', 'track' ) : {
                    'desc' : 'Repopulate the track number in each disc',
                    'func' : cmd_populate_track_no
                }
            },
            "Regex" : {
                ( 'ab', 'album', 'at', 'artist', 'atva' ) : {
                    'desc' : 'Set the album name or album artist',
                    'func' : cmd_set_album,
                },
                ( 'ta', 'tt' ) : {
                    'desc' : "Set the track's artist or title",
                    'func' : cmd_set_track,
                },
                ( 'dta', 'dtt' ) : {
                    'desc' : "Set the ( disc, track )'s artist or title",
                    'func' : cmd_set_disc_track,
                },
                ( 'rea', 'ret' ) : {
                    'desc' : 'Set the artist or title of all files using regular expression',
                    'func' : cmd_set_track_regex,
                }
            }
        }

        for album in sorted( self.albums.values(), key=lambda x: str( x.path.name ) ):
            if self.skip_complete and album.ready_to_copy():
                continue
            album.show_content()
            if self.dry_run:
                continue
            while True:
                cmd = get_input( func_map )
                if cmd in [ 'q', 'quit' ]:
                    return
                if cmd in [ 'h', 'help' ]:
                    cmd_help( func_map )
                elif dispatcher( func_map, cmd, album ):
                    if cmd in [ 'n', 'next' ]:
                        del self.albums[ album.path ]
                    break

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
        self.load_audio_files()
        self.show_summary()
        self.command_prompt()
        self.show_summary()

class RoonCopyCmd( CleanupCmd ):
    '''The command to copy complete albums to Roon library'''
    def load_audio_files( self ):
        '''Load all flac files'''
        corrupted = []

        cwd = Path( self.location )
        for filename in list( cwd.glob( '**/*.flac' ) ):
            flac = AudioFile( self.config, filename )
            if not flac.initialized:
                corrupted.append( flac )
                continue
            if flac.album_path() not in self.albums:
                self.albums[ flac.album_path() ] = \
                        Album( self.config, flac.album_path() )
            self.albums[ flac.album_path() ].add_track( flac )

        self.albums = { path : album for path, album in self.albums.items()
                        if album.ready_to_copy( target=self.flac_target ) }

        corrupted = [ f.album_path() for f in corrupted ]
        if not corrupted:
            return
        for path in corrupted:
            if path in self.albums:
                print( f'Skipping corrupted album {path}' )
                del self.albums[ path ]

    def roon_copy( self ):
        '''Copy all complete albums to Roon library'''
        for album in self.albums.values():
            various_artists = 'Various Artists'
            folder_name = str( album.path.name )
            src = album.path.absolute()

            dst = self.config[ 'Roon Library' ][ 'Location']
            dst = os.path.join( dst, self.flac_target )
            if self.flac_target in [ 'cd', 'flac' ]:
                if album.album_artist() == various_artists:
                    dst = os.path.join( dst, various_artists )
                else:
                    initial = album.album_artist()[ 0 ]
                    initial = '0' if ord( initial ) >= ord( 'a' ) and \
                              ord( initial ) <= ord( '9' ) else initial
                    dst = os.path.join( dst, initial, album.album_artist() )
            elif self.flac_target in [ 'mqa', 'Thai' ]:
                if album.album_artist() == various_artists:
                    dst = os.path.join( dst, various_artists )
                else:
                    dst = os.path.join( dst, album.album_artist() )
            dst = os.path.join( dst, folder_name )

            if os.path.exists( dst ):
                print( f'Skipped {folder_name}' )
                continue

            if self.verbose or self.dry_run:
                print( f'Copy "{src}" to "{dst}"' )

            try:
                if not self.dry_run:
                    shutil.copytree( src, dst )
            except ( FileNotFoundError, PermissionError, shutil.Error ) as exception:
                print( exception )

    def run( self ):
        self.load_audio_files()
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
        archive_dst = self.config[ 'Extract' ][ 'Archive' ]
        for fmt in self.config[ "Extract" ][ "Archive Format" ]:
            cmds += [ ExtractCmd( self.config, f, params ) for f in cwd.glob( f'**/*{fmt}' )
                      if archive_dst not in str( f.absolute() ) ]
        if cmds and not params.dry_run():
            os.makedirs( params.archive_dst(), exist_ok=True )
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec() )

    def convert_audio( self, params ):
        '''Convert the autio files to .flac'''
        cwd = Path( os.getcwd() )
        cmds = []
        for fmt in self.config[ "Extract" ][ "Convert Format" ]:
            cmds += [ ConvertCmd( self.config, f, params ) for f in cwd.glob( f'**/*{fmt}' ) ]
        self.execute_commands( execute, cmds, seq_exec=params.seq_exec() )

    def cleanup( self, params ):
        '''Do various data cleanup on all folders in the current folder'''
        cmds = [ CleanupCmd( self.config, os.getcwd(), params ) ]
        self.execute_commands( execute, cmds )

    def roon_copy( self, params ):
        '''Do various data cleanup on all folders in the current folder'''
        cmds = [ RoonCopyCmd( self.config, os.getcwd(), params ) ]
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
    flac_target = config[ 'Copy' ][ 'Flac Target' ]

    parser = argparse.ArgumentParser()
    parser.add_argument( '-d', '--dry-run', action='store_true', dest='dry_run',
                         help='Dry run' )
    parser.add_argument( '-s', '--seq-exec', action='store_true', dest='seq_exec',
                         help='Use sequential execution' )
    parser.add_argument( '-t', '--target', action='store',
                         dest='target', default=flac_target,
                         choices=[ 'cd', 'dsd', 'flac', 'mqa', 'Thai' ],
                         help='Set the flac target for Roon' )
    parser.add_argument( '-v', '--verbose', action='store_true', dest='verbose',
                         help='Print debug info' )

    subparser = parser.add_subparsers( dest='command' )
    subparser.required = True

    cleanup_parser = subparser.add_parser( 'cleanup', help='Do various data cleanup' )
    cleanup_parser.add_argument( '-k', '--skip-complete', action='store_true',
                                 help='Skip the cleaned album' )
    subparser.add_parser( 'extract', help='Extract compressed archives' )
    subparser.add_parser( 'convert', help='Convert audio files to .flac' )
    subparser.add_parser( 'copy', help='Copy complete albums to Roon library' )

    args = parser.parse_args()
    params_dict = {
        "command" : args.command,
        "dry_run" : args.dry_run,
        "verbose" : args.verbose,
        "seq_exec" : False if args.command in [ 'cleanup', 'copy' ] \
                     else args.seq_exec,
        "skip_complete" : getattr( args, 'skip_complete', False ),
        "flac_target" : getattr( args, 'target', flac_target ),
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
