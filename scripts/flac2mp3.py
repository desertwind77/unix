#!/usr/bin/env python3

from pprint import pprint
import argparse
import os
import re
import sys

from pydub import AudioSegment

class CopyInfo:
    '''Command to copy the source file to the destination file'''
    def __init__( self, src, dst ):
        self.src = src
        self.dst = dst

    def __str__( self ):
        return f'{self.src} ---> {self.dst}'

def process_arguments():
    '''Parse command line agruments'''
    parser = argparse.ArgumentParser()
    parser.add_argument( "dst", action="store", help="Destination foler" )
    parser.add_argument( "folders", nargs="*", help="Folders containing flac files" )
    parser.add_argument( "-p", "--preserve", action="store_true",
                         help="Preserve the folder structure" )
    parser.add_argument( "-d", "--dry-run", action="store_true",
                         help="Do not the conversion" )
    return parser.parse_args()

def process_all_folders( dst, folders, preserve_dir_structure=False ):
    '''Process all the folders in the arguments and return the list of (src,dst)'''
    def sanity_check( folder ):
        contents = os.listdir( folder )
        keyword_cd  = any( 'cd' in c.lower() for c in contents )
        keyword_disc = any( 'disc' in c.lower() for c in contents )
        keyword_flac = any( '.flac' in c.lower() for c in contents )
        assert not ( keyword_cd and keyword_disc ), \
                "CD and Disc are mutually exclusive"
        assert not ( ( keyword_cd or keyword_disc ) and keyword_flac ), \
                "CD/Disc and .flac are mutually exclusive"

    def contain_subfolder( folder ):
        contents = os.listdir( folder )
        return any( 'cd' in c.lower() for c in contents ) or \
                any( 'disc' in c.lower() for c in contents )

    def list_flacs( folder ):
        flacs = [ f for f in os.listdir( folder ) if f.endswith( '.flac' ) ]
        return sorted( flacs )

    for folder in folders:
        sanity_check( folder )

    copy_info = []
    for folder in folders:
        flacs = None
        if contain_subfolder( folder ):
            subfolders = [ d for d in os.listdir( folder ) \
                           if os.path.isdir( os.path.join( folder, d ) ) and 'Disc' in d ]
            if not subfolders:
                subfolders = [ d for d in os.listdir( folder ) \
                           if os.path.isdir( os.path.join( folder, d ) ) and 'CD' in d ]

            flacs = {}
            for subfolder in subfolders:
                flacs[ subfolder ] = list_flacs( os.path.join( folder, subfolder ) )
        else:
            flacs = list_flacs( folder )

        if not flacs:
            continue

        def get_copy_info( dst, folder, flac, subfolder=None, prefix=None ):
            mp3 = os.path.splitext( flac )[ 0 ] + '.mp3'
            if subfolder and prefix:
                # We don't dont have any CD collections with more than 99 CDs.
                # So a two-digit prefix is OK.
                mp3 = f'{prefix:02}_{mp3}'
                mp3 = os.path.join( dst, folder, mp3 )
                flac = os.path.join( folder, subfolder, flac )
            else:
                mp3 = os.path.join( dst, folder, mp3 )
                flac = os.path.join( folder, flac )

            return CopyInfo( flac, mp3 )

        if isinstance( flacs, dict ):
            for subfolder, filelist in flacs.items():
                if preserve_dir_structure:
                    for flac in filelist:
                        all_folder = os.path.join( folder, subfolder )
                        copy_info.append( get_copy_info( dst, all_folder, flac ) )
                else:
                    obj = re.search( r'Disc (\d+)', subfolder )
                    if not obj:
                        obj = re.search( r'CD (\d+)', subfolder )
                    disc_no = int( obj.group( 1 ) )
                    for flac in filelist:
                        copy_info.append( get_copy_info( dst, folder, flac,
                                                         subfolder=subfolder, prefix=disc_no ) )
        elif isinstance( flacs, list ):
            for flac in flacs:
                copy_info.append( get_copy_info( dst, folder, flac ) )
        return copy_info

def convert( info ):
    '''Convert from flac to mp3'''
    path = os.path.split( info.dst )[ 0 ]
    if not os.path.exists( path ):
        os.makedirs( path )

    flac = AudioSegment.from_file( info.src, format="flac" )
    flac.export( info.dst, format="mp3" )

def convert_all_files( dst, copy_info, dry_run=False ):
    '''Convert all the files in copy_info'''
    if not dry_run and not os.path.exists( dst ):
        # Recursively make the directory where os.mkdir() is the
        # non-recersive counterpart
        os.makedirs( dst )

    size = len( copy_info )
    digits = len( str( size ) )
    for count, info in enumerate( copy_info ):
        count_str = str( count + 1 ).rjust( digits, '0' )
        print( f'{count_str}/{size}', info )
        if not dry_run:
            convert( info )
def main():
    '''Main program'''
    args = process_arguments()
    copy_info = process_all_folders( args.dst, args.folders, args.preserve )
    convert_all_files( args.dst, copy_info, args.dry_run )

if __name__ == '__main__':
    main()
