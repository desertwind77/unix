# audioli.py : python library for managing audio files
#
# Note to print docstring
# import audiolib.py
# print repr( audiolib.isSupportedFormat.__doc__ )
# print audiolib.LastFmHelper.getSearchQuery.__doc__
import json
import os
import re
import shutil
import subprocess
import urllib
import urllib2

from debuglib import t0, t1

########################### Global Variable ###########################
# Last.fm api info
lastfm_info = {
        'ApplicationName' : 'AllPlayer',
        'ApiKey' : '12181a843fffcf3e27ef09557247ac25',
        'SharedSecret' : '12181a843fffcf3e27ef09557247ac25',
        'RegisteredTo' : 'athichart',
        }
api_key = lastfm_info[ 'ApiKey' ]

supportedAudioFormat = [ '.mp3', '.flac' ]

class NotImplemented( Exception ):
    def __str__( self ):
        return "This method must be implemented in a derived class"

########################### Classes for managing Last.fm data ########################### 

class LastFmHelper( object ):
    def __init__( self ):
        self._lastFmData = None
        self._downloadedData = None

    def getSearchQuery( self ):
        """Generate url for querying Last.fm"""
        raise NotImplemented

    def getLastFmData( self ):
        """Query Last.fm if not yet done; otherwise, return cached data"""
        if self._lastFmData:
            return self._lastFmData

        url = self.getSearchQuery() 
        try:
            response = urllib2.urlopen( url )
        except urllib2.HTTPError as h:
            if h.code == 400:
                t0( url )
            
            t0( h.code )
            t0( h.msg )
        data = response.read()
        self._lastFmData = json.loads( data )
        return self._lastFmData

    def getBaseDir( self ):
        """Get the base directory of the desired data of the json retrieved from Last.fm."""
        raise NotImplemented

    def getCoverUrl( self ):
        """Get url to the cover art or None"""
        lastFmData = self.getLastFmData()
        if not lastFmData:
            return None
        baseDir = lastFmData.get( self.getBaseDir() )
        if not baseDir:
            return None
        imageList = baseDir.get( 'image' )
        if not imageList:
            return None

        sizeList = [ 'extralarge', 'large', 'medium', 'small' ]
        for size in sizeList:
            for img in imageList:
                if img[ 'size' ] == size:
                    return img[ '#text' ]
        return None

    def getCover( self ):
        """Get the location on the filesystem of the downloaded cover art or None"""
        if self._downloadedData: 
            return self._downloadedData

        url = self.getCoverUrl()
        if not url:
            return None

        cmd = "wget -q -P /tmp %s" % url
        subprocess.call( cmd, shell=True )

        filename = url.split( '/' )[ -1 ]
        self._downloadedData = "/tmp/%s" % filename
        return self._downloadedData

# ArtistInfo is used to download an artist image from LastFm
class ArtistInfo( LastFmHelper ):
    def __init__( self, artist ):
        LastFmHelper.__init__( self )
        self.artist = artist

    def __repr__( self ):
        return self.artist

    def __str__( self ):
        return self.artist

    def getSearchQuery( self ):
        """Generate url for querying Last.fm"""
        urlFormat = 'https://ws.audioscrobbler.com/2.0/?method=artist.getinfo'
        urlFormat += '&api_key=%s&%s&format=json'
        query_args = { 'artist' : self.artist }
        query_string = urllib.urlencode( query_args )
        url = urlFormat % ( api_key, query_string )
        return url

    def getBaseDir( self ):
        """Get the base directory of the desired data of the json retrieved from Last.fm."""
        return 'artist'

# AlbumInfo is used to download album-related info e.g. cover art and
# track info from Last.fm using the combinatio of artist and album 
# as a key to search
class AlbumInfo( LastFmHelper ):
    def __init__( self, artist, album ):
        LastFmHelper.__init__( self )
        self.artist = artist
        self.album = album

    def __repr__( self ):
        return "%s - %s" % ( self.artist, self.album )

    def __str__( self ):
        return "%s - %s" % ( self.artist, self.album )

    def getSearchQuery( self ):
        """Generate url for querying Last.fm"""
        urlFormat = 'https://ws.audioscrobbler.com/2.0/?method=album.getinfo'
        urlFormat += '&api_key=%s&%s&format=json'
        query_args = { 'artist' : self.artist, 'album' : self.album }
        query_string = urllib.urlencode( query_args )
        url = urlFormat % ( api_key, query_string ) 
        return url

    def getBaseDir( self ):
        """Get the base directory of the desired data of the json retrieved from Last.fm."""
        return 'album'

    def getTrackList( self ):
        """Get the list of the tracks in the album"""
        lastFmData = self.getLastFmData()
        tracks = lastFmData[ 'album' ][ 'tracks' ][ 'track' ]
        trackList = {} 
        for t in tracks:
            trackNo = t[ '@attr' ][ 'rank' ]
            name = t[ 'name' ]
            trackList[ trackNo ] = name
        return trackList

    def getTrackTitle( self, track ):
        """Get the track title"""
        title = None
        trackList = self.getTrackList()
        if trackList:
            title = trackList.get( track )  
        return title 

########################### Classes for managing audio files ########################### 

# FileInfo holds the information about a particular file.
# The derived classes will take care of saving tags for the
# corresponding file types.
class FileInfo( object ):
    def __init__( self, filename, artist=None, album=None, title=None, disc=None,
                  track=None, cover=None, downloadType=None ):
        self.filename = filename
        self.artist = artist
        self.album = album
        self.title = title
        self.disc = disc
        self.track = track
        self.cover = cover
        self.downloadType = downloadType

    def __repr__( self ):
        return 'FileInfo(%s)' % os.path.basename( self.filename )

    def __str__( self ):
        return "( %s, %s, %s, %s, %s, %s, %s, %s )" % \
                ( os.path.basename( self.filename ), self.artist,
                  self.album, self.disc, self.track, self.title,
                  self.cover, self.downloadType )

    def getProperty( self, tag ):
        """Get the value of a class member which happens to be identical to the tag"""
        result = self.__dict__.get( tag ) 
        return result

    def getCoverPhoto( self, albumArtistInfo=None ):
        """
        Download the cover art from Last.fm and return the location
        on the filesystem or return None
        """
        coverPhoto = None

        if self.cover:
            coverPhoto = self.cover
        elif self.downloadType:
            if self.downloadType == 'artist' and self.artist:
                if not albumArtistInfo:
                    artistInfo = ArtistInfo( self.artist ) 
                coverPhoto = artistInfo.getCover() 
            elif self.downloadType == 'album' and self.artist and self.album:
                if not albumArtistInfo:
                    albumArtistInfo = AlbumInfo( self.artist, self.album )
                coverPhoto = albumArtistInfo.getCover()

        return coverPhoto

    def rename( self, renameRegex, dryRun=False ):
        """Rename the file based on rename regex"""
        newName = None
        dirName = os.path.dirname( self.filename )
        _, ext = os.path.splitext( self.filename )

        tagPattern = r'<\w*>'
        tagSearch = re.findall( tagPattern, renameRegex )
        for t in tagSearch:
            tokenSearch = re.match( r'<(.*)>', t )
            if not tokenSearch:
                assert False
            tokenName = tokenSearch.group( 1 )
            replacement = self.getProperty( tokenName )
            if not replacement:
                t0( 'Warning : skipped renaming %s (tag %s not found)' % \
                        ( self.filename, tokenName ) )
                return

            # Do a little cleanup for title
            if 'title' in tokenName:
                # Capitalize properly
                replacement = replacement.title()
                # Remove tailing space
                replacement = replacement.rstrip()
            renameRegex = re.sub( t, replacement, renameRegex )

        newName = '%s/%s%s' % ( dirName, renameRegex, ext )
        t0( newName )

        if os.path.exists( newName ):
            t0( "Warning : skipping rename %s already exists" % self.filename )
            return

        t0( "Renaming : %s" % self.filename )
        t1( "src = %s" % self.filename )
        t1( "dst = %s" % newName )
        if not dryRun:
            os.rename( self.filename, newName )
        self.filename = newName

    def save( self, albumArtistInfo=None, dryRun=False ):
        """Save all tags to the file"""
        raise NotImplemented

    def dump( self ):
        """Dump all tags in the file"""
        raise NotImplemented

    def getTag( self, tag ):
        """Get a tag from the file"""
        raise NotImplemented

class MP3FileInfo( FileInfo ):
    def __repr__( self ):
        return 'MP3FileInfo(%s)' % os.path.basename( self.filename )

    # If albumInfo is not None, we use the album cover in albumInfo.
    # Otherwise, if createAlbumInfo=True and artist and title are
    # available, we create a new albumInfo by ourself.
    #
    # Reason : when we process a directory that contains multiple
    # songs from the same album, we don't want to download album
    # cover for all the songs. One download is enough.
    def save( self, albumArtistInfo=None, dryRun=False ):
        """Save all tags to the file"""
        # Generate options for eyeD3
        options = ''
        if self.artist:
            options += '-a "%s" ' % self.artist
        if self.album:
            options += '-A "%s" ' % self.album
        if self.title:
            options += '-t "%s" ' % self.title
        if self.disc:
            options += '-d "%s" ' % self.disc
        if self.track:
            options += '-n "%s" ' % self.track
        coverPhoto = self.getCoverPhoto( albumArtistInfo )
        if coverPhoto:
            options += '--add-image %s:FRONT_COVER' % coverPhoto

        t0( 'Tagging %s : ( %s, %s, %s, %s, %s, %s )' % ( self.filename,
            self.artist, self.album, self.disc, self.track,
            self.title, coverPhoto ) )

        cmd = 'eyeD3 %s "%s"' % ( options, self.filename )
        t1( cmd )
        if not dryRun:
            subprocess.call( cmd, shell=True )
            t0()

    def dump( self ):
        """Dump all tags in the file"""
        from mutagen.easyid3 import EasyID3
        tagInfo = EasyID3( self.filename )
        t0( "Title  = ", tagInfo.get( 'title' ) )
        t0( "Artist = ", tagInfo.get( 'artist' ) )
        t0( "Album  = ", tagInfo.get( 'album' ) )
        t0( "Track  = ", tagInfo.get( 'tracknumber' ) )
        t0( "Disc   = ", tagInfo.get( 'discnumber' ) )

    def getTag( self, tag ):
        """Get a tag from the file"""
        pass

class FlacFileInfo( FileInfo ):
    def __repr__( self ):
        return 'FlacFileInfo(%s)' % os.path.basename( self.filename )

    def isCoverExist( self, audio ):
        if audio.pictures:
            return True

        if 'covr' in audio or 'APIC:' in audio:
            return True
        
        return False

    def save( self, albumArtistInfo=None, coverOnly=False, dryRun=False ):
        """Save all tags to the file"""
        def generateCoverPhoto( coverPhoto ):
            image = Picture()
            image.type = 3
            if coverPhoto.endswith( 'png' ):
                image.mime = 'image/png'
            elif coverPhoto.endswith( 'jpg' ):
                image.mime = 'image/jpeg'
            image.desc = 'front cover'
            with open( coverPhoto, 'rb' ) as f:
                image.data = f.read()

            return image

        from mutagen.flac import Picture, FLAC
        audio = FLAC( self.filename )
        if not coverOnly:
            if self.title: 
                audio[ 'title' ] = self.title
            if self.artist:
                audio[ 'artist' ] = self.artist
            if self.album:
                audio[ 'album' ] = self.album
            if self.track:
                audio[ 'tracknumber' ] = self.track
            if self.disc:
                audio[ 'discnumber' ] = self.disc
        coverPhoto = self.getCoverPhoto( albumArtistInfo )
        if coverPhoto:
            if self.isCoverExist( audio ):
                audio.clear_pictures()
            coverPhotoImage = generateCoverPhoto( coverPhoto )
            audio.add_picture( coverPhotoImage )
        elif coverOnly:
            t0( 'Skipping : %s (coverOnly but not cover found)' % self.filename )
            return

        t0( 'Tagging : %s' % self.filename )
        t1( 'Artist = %s %s' % ( self.artist, '(no change)' if coverOnly else '' ) )
        t1( 'Album  = %s %s' % ( self.album, '(no change)' if coverOnly else '' ) ) 
        t1( 'Disc   = %s %s' % ( self.disc, '(no change)' if coverOnly else '' ) ) 
        t1( 'Track  = %s %s' % ( self.track, '(no change)' if coverOnly else '' ) )
        t1( 'Title  = %s %s' % ( self.title, '(no change)' if coverOnly else '' ) )
        t1( 'Cover  =', coverPhoto )
        if not dryRun:
            t0( 'Saved' )
            audio.save()

    def dump( self ):
        """Dump all tags in the file"""
        from mutagen.flac import FLAC
        audio = FLAC( self.filename )
        tagList = [ 'title', 'artist', 'album', 'tracknumber', 'discnumber'  ]
        for key in tagList:
            value = audio.get( key )
            if value:
                t0( "%s = %s" % ( key, value[ 0 ] ) )
        t0( "Cover = %s" % self.isCoverExist( audio ) )

    def getTag( self, tag ):
        """Get a tag from the file"""
        def translateTag( tag ):
            translate = { 'disc' : 'discnumber',
                          'track' : 'tracknumber',
                          }
            result = translate.get( tag )
            if result:
                return result
            return tag

        from mutagen.flac import FLAC
        audio = FLAC( self.filename )
        result = audio.get( translateTag( tag ) )
        if result:
            return result[ 0 ]
        t0( 'Warning : %s does not contain tag <%s>.' % \
                ( self.filename, tag ) )
        return None

########################### Utilities functions ########################### 

def getSupportedAudioFormat():
    """Return the list of supported file formats"""
    return supportedAudioFormat

def getAudioFormat( filename ):
    """Return audio format if supported; otherwise None"""
    for f in getSupportedAudioFormat():
        searchString = f
        if searchString in filename:
            return f
    return None

def isSupportedFormat( filename ):
    """Check if the file is supported or not"""
    _, ext = os.path.splitext( filename )
    if ext in getSupportedAudioFormat():
        return True
    return False

def createFileInfo( fullname, artist=None, album=None, title=None, disc=None,
                    track=None, cover=None, downloadType=None ):
    """Create a FileInfo object for a particular file type"""
    fileInfoDict = {
            '.flac' : FlacFileInfo,
    # Currently not supported
    #        '.mp3' : MP3FileInfo,
            }

    _, ext = os.path.splitext( fullname )
    ext = ext.lower()
    fileInfo = fileInfoDict.get( ext )
    assert fileInfo
    return fileInfo( fullname, artist, album, title, disc, track,
                     cover, downloadType )
