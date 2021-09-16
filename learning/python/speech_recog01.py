#!/usr/bin/env python3
'''
We need to install SpeechRecognition and PyAudio
sudo pip3 install SpeechRecognition PyAudio
'''

import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print( 'Say anything : ' )
    audio = r.listen( source )
    try:
        text = r.recognize_google( audio )
        print( 'You said : {}'.format( text ) )
    except:
        print( 'Sorry' )
