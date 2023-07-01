#!/usr/bin/env python
import os
import re

from debuglib import setDebugLevel, t0, t1, t2, pprint1

def cleanupFilename( string ):
    """Clean up source filename e.g. removing certain characters"""
    t2( "Entering", cleanupFilename.__name__ )

    t2( "before :", string )
    replacement = { '`' : '\'',
                    '_' : ' ',
                    '\+' : ' ',
                  }
    for k, v in replacement.items():
        string = re.sub( k, v, string )
    t2( "after  :", string )

    t2( "Leaving", cleanupFilename.__name__ )
    return string

def cleanupRegex( string ):
    """Clean up the input regex"""
    t2( "Entering", cleanupRegex.__name__ )

    # Note : 
    # Currently, we use this function to clean up only srcRegex.
    # Not sure if we need to clean up dstRegex or not.
    # So far, there has been no need.
    t2( "before :", string )
    # Replace '(' and ')' with '\(' and '\)' respectively
    replacement = { '(' : '\(', 
                    ')' : '\)', 
                    '[' : '\[',
                    ']' : '\]',
                    '.' : '\.',
                   }
    for key, value in replacement.items():
        pos = string.find( key )
        while pos >= 0:
            string = string[ 0 : pos ] + value  + string[ pos + 1: ]
            pos = string.find( key, pos + 2 )
    t2( "after  :", string )

    t2( "Leaving", cleanupRegex.__name__ )
    return string

def regexParse( regex, txt ):
    '''
    Extract filed/tag from txt. Return value is the dict of
    fields and their value
    '''
    t2( "Entering", regexParse.__name__ )

    def isNumField( field ):
        """Check if field is a numeric field or not"""
        predefinedNumFields = [ 'num', 'track' ]
        for i in predefinedNumFields:
            if i in field:
                return True
        return False

    # Pre-processing regex and txt
    regexDict = {}
    regex = cleanupRegex( regex )
    regex = r'%s' % regex
    txt = cleanupFilename( txt )

    # Build regexDict from regex
    tagField  = r'<\w*>'
    numField  = r'(\d+)'
    # charField try to match  Words starting with "0-9", "a-zA-Z",
    # "-", "&", "'", ",", "." and space.
    charField = r'([\d\w\-&\'\(\)\. ,]+)'

    searchResult = re.findall( tagField, regex )
    i = 0
    for s in searchResult:
        i += 1
        tokenSearch = re.match( r'<(.*)>', s )
        assert tokenSearch
        tokenName = tokenSearch.group( 1 )

        # regexDict maps between tokenName (tag) and its position in
        # regex to help tag replacement later
        regexDict[ tokenName ] = i

        # Replace the token with regular expression to match
        # the token.
        if isNumField( tokenName ):
            regex = re.sub( s, numField, regex ) 
        else:
            regex = re.sub( s, charField, regex ) 
        
    # Parse txt with regex
    t1( "txt     :", txt )
    t1( "regex   :", regex )
    searchResult = re.match( regex, txt )
    if not searchResult:
        # Not match
        t1( 'Warning : no match found' )
        return None

    # regex and txt match. So try to determine the field/tag value.
    fieldDict = {}
    for key, value in regexDict.iteritems():
        fieldDict[ key ] = searchResult.group( value )

    t1( "dict   :" )
    pprint1( fieldDict )

    t2( "Leaving", regexParse.__name__ )
    return fieldDict 

def regexReplace( regex, fieldDict ):
    t2( "Entering", regexReplace.__name__ )
    t1( "before :", regex )

    tagField  = r'<\w*>'
    searchResult = re.findall( tagField, regex )
    for p in searchResult:
        tokenSearch = re.match( r'<(.*)>', p )
        assert tokenSearch

        tokenName = tokenSearch.group( 1 )
        replacement = fieldDict.get( tokenName ) 
        if not replacement:
            t0( "Error: tag <%s> is not available" % tokenName )
            return None
        # Do some cleanup e.g. capitalizing and removing tailing space
        if 'title' in tokenName:
            replacement = replacement.title()
            replacement = replacement.rstrip()
        regex = re.sub( p, replacement, regex )

    t1( "after  :", regex )
    t2( "Leaving", regexReplace.__name__ )
    return regex

def regexRename( srcRegex, dstRegex, src ):
    t2( "Entering", regexRename.__name__ )

    fieldDict = regexParse( srcRegex, src )
    if not fieldDict:
        return None

    result = regexReplace( dstRegex, fieldDict )
    t1( "result :", result )

    t2( "Leaving", regexRename.__name__ )
    return result 

#################### Test cases ##################
testSuite = [
    # Test 0
    { "id"  : 0,
      "src" : "11 What's This I Find",
      "dst" : "1-11 What's This I Find",
      "srcRegex" : "<rest>",
      "dstRegex" : "1-<rest>",
      "enable"   : True },
    # Test 1
    { "id"  : 1,
      "src" : "1-11 What's This I Find",
      "dst" : "11 What's This I Find",
      "srcRegex" : "1-<rest>",
      "dstRegex" : "<rest>",
      "enable"   : True },
    # Test 2
    { "id"  : 2,
      "src" : "03 Pachelbel  Canon & Gigue in D major (Canon & Gigue in D major) - Jean-Francois Paillard",
      "dst" : "03 Jean-Francois Paillard - Pachelbel's Canon & Gigue in D major",
      "srcRegex" : "<track> <Composer>  <Song1> (<Song2>) - <Artist>",
      "dstRegex" : "<track> <Artist> - <Composer>'s <Song1>",
      "enable"   : True },
    # Test 3
    { "id"  : 3,
      "src" : "10.DIONYSUS- Don`t Forget",
      "dst" : "10 Dionysus- Don't Forget",
      "srcRegex" : "<track>.<title>-<Song>",
      "dstRegex" : "<track> <title>-<song>", 
      "enable"   : True },
    # Test 4
    { "id"  : 4,
      "src" : "19.AXEL RUDI PELL - Live For The King",
      "dst" : "19 Axel Rudi Pell - Live For The King",
      "srcRegex" : "<track>.<title> - <Song>",
      "dstRegex" : "<track> <title> - <song>",
      "enable"   : True },
    # Test 5
    { "id"  : 5,
      "src" : "210_michael_monroe_-_dead,_jail_or_rock_n_roll",
      "dst" : "210 Michael Monroe - Dead, Jail Or Rock N Roll",
      "srcRegex" : "<track> <title> - <SongTitle>",
      "dstRegex" : "<track> <title> - <SongTitle>", 
      "enable"   : True },
    # Test 6
    { "id"  : 6,
      "src" : "213_metallica_-_welcome_home_(sanitarium)",
      "dst" : "213 Metallica - Welcome Home (Sanitarium)",
      "srcRegex" : "<track> <title> - <SongTitle>",
      "dstRegex" : "<track> <title> - <SongTitle>", 
      "enable"   : True },
    # Test 7 : just want to add ( and ) in to dstRegex
    { "id"  : 7,
      "src" : "213_metallica_-_welcome_home_(sanitarium)",
      "dst" : "(213) (Metallica) - (Welcome Home (Sanitarium))",
      "srcRegex" : "<track> <title> - <SongTitle>",
      "dstRegex" : "(<track>) (<title>) - (<SongTitle>)", 
      "enable"   : True },
    # Test 8
    { "id"  : 8,
      "src" : "[02].Beautiful (Christina Aguilera)",
      "dst" : "02 Christina Aguilera - Beautiful",
      "srcRegex" : "[<track>].<song> (<artist>)",
      "dstRegex" : "<track> <artist> - <song>", 
      "enable"   : True },
    # Test 9
    { "id"  : 9,
      "src" : "Etude_Opus_76_No._2_in_D_Major",
      "dst" : "Etude Opus 76 No. 2 in D Major",
      "srcRegex" : "<all>",
      "dstRegex" : "<all>",
      "enable"   : True },
    # Test 10 : clean up "_" in the filename. Capitilaztion is too hard.
    { "id"  : 10,
      "src" : "J.S.Bach_Sarabande_from_Partita_for_solo_violin_No1_h-moll_BWV_1002._Arranged_for_guitar_by_A._Segovia.",
      "dst" : "J.S.Bach Sarabande from Partita for solo violin No1 h-moll BWV 1002. Arranged for guitar by A. Segovia.",
      "srcRegex" : "<all>",
      "dstRegex" : "<all>",
      "enable"   : True },
    # Test 11 : known failures because of ambiguity. 
    # 'composer': 'Tchaikovsky  Swan Lake',
    # 'song1': 'Act 2 Scene',
    { "id"  : 11,
      "src" : "24 Tchaikovsky  Swan Lake  Act 2 Scene [Swan Theme Excerpt] (Swan Lake  Act 2 Scene Swan Theme Excerpt) - Alexander Lazarev",
      "dst" : "24 Alexander Lazarev - Tchaikovsky - Swan Lake  Act 2 Scene Swan Theme Excerpt)",
      "srcRegex" : "<track> <composer>  <song1> [<xxx>] (<song2>) - <artist>",
      "dstRegex" : "<track> <artist> - <composer> - <song2>",
      "enable"   : False },
]

def test():
    selectedTests = list( range( len( testSuite ) ) ) 
    # Uncomment the following line to test just a specific testcase
    #selectedTests = [ 9 ]

    for i in selectedTests:
        t = testSuite[ i ]
        if not t[ 'enable' ]:
            continue

        srcRegex = t[ 'srcRegex' ].lower()
        dstRegex = t[ 'dstRegex' ].lower()
        src = t[ 'src' ]
        dst = t[ 'dst' ]
        t1( "testcase : %d" % t[ 'id' ] )
        output = regexRename( srcRegex, dstRegex, src ) 
        t1( "expected : %s" % dst )
        t1( "received : %s" % output )
        t1() 

        assert dst == output

    t0( 'All test passed' )

def main():
    import argparse

    parser = argparse.ArgumentParser( version='1.0',
                                      description='regexlib parser' )
    parser.add_argument( '-B', '--debugLevel', action='store', dest='debugLevel',
            type=int, help='Set debug level' )
    args = parser.parse_args()

    if args.debugLevel:
        setDebugLevel( args.debugLevel )

    test()

if __name__ == '__main__':
    main()
