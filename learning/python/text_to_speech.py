#!/usr/bin/env python3
'''
Text to speach using gtts

Need to install gTTS
pip install gTTS

Reference:
gtts.readthedocs.io/en/stable/index.html
'''

from gtts import gTTS
import os

myText = "Text to Speech Coversion Using Python"
fh = open( "text_to_speech_test.txt", "r" )
fh.read().replace( "\n", " " )
language = 'en'
output = gTTS( text=myText, lang=language, slow=False )
output.save( "output.mp3")
fh.close()

# This is for Mac OS X
#os.system( "afplay output.mp3" )
