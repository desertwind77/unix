#!/usr/bin/env python
import argparse
import getopt
import os
import re
import shutil
import sys

from debuglib import t0, t1, t2, pprint1

junkFileList = [ '.DS_Store', '.wdmc', '.fseventsd', '.Spotlight-V100' ]

def folderExists( path ):  
    '''Check if path exists and is a folder, not file'''
    if not os.path.exists( path ) or not os.path.isdir( path ):
        return False
    return True

def moveFile( src, dst, dryRun=False ):
    '''Move file from src to dst'''
    if os.path.exists( dst ):
        t0( "Warning : %s skipped renaming %s (already exists)" % \
                ( moveFile.__name__, dst ) )
        return

    if not dryRun:
        shutil.move( src, dst )
