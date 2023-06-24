import json
import os

# A formatted string literal or f-string is a string literal
# that is prefixed with 'f' or 'F'. These strings may contain
# replacement fields, which are expressions delimited by curly
# braces {}. While other string literals always have a constant
# value, formatted strings are really expressions evaluated
# at run time.

class FileNotFound( Exception ):
    """Raised when a file is not found"""
    def __init__( self, filename ):
        self.filename = filename
        message = f'File {self.filename} not found'
        super().__init__( message )

class DirectoryNotFound( Exception ):
    """Raised when a folder is not found"""
    def __init__( self, folder ):
        self.folder = folder
        message = f'Folder {self.folder} not found'
        super().__init__( message )

def check_if_file_exists( filename ):
    '''Check if the file exists'''
    if not os.path.exists( filename ) or not os.path.isfile( filename ):
        raise FileNotFound( filename )

def check_if_folder_exists( folder ):
    '''Check if the folder exists'''
    if not os.path.exists( folder ) or not os.path.isdir( folder ):
        raise DirectoryNotFound( folder )

def load_config( config_filename, verbose=False ):
    '''Load the configuration file'''
    # __file__ stores the absolute path of the python script
    # realpath() return the canonical path of the specified
    # filename by eliminating any symbolic links encountered
    # in the path
    script_path = os.path.realpath( os.path.dirname( __file__ ) )
    config_abs_filename = os.path.join( script_path, config_filename )
    check_if_file_exists( config_abs_filename)

    config = None
    with open( config_abs_filename, encoding="utf-8" ) as config_file:
        if verbose:
            print( f'Loading config file: {config_abs_filename}' )
        config_data = json.load( config_file )
        config = config_data.get( 'config', None )

    if config and "Destinations" in config:
        destinations = config[ "Destinations" ]
        for _, folder in destinations.items():
            check_if_folder_exists( folder )
    return config
