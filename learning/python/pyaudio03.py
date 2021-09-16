#!/usr/bin/env python3
from pyaudio import PyAudio, paFloat32, paContinue
from numpy import zeros, sin, pi, arange, array, concatenate, float32
import time

def generateSamples( samplingRateInHz, durationInSec, freqInHz, volume ):
    ''' Generate samples and convert to a float32 array

    Parameters
        samplingRateInHz        sampling rate in Hz
        durationInSec           duration of the samples in sec
        freqInHz                note frequency in Hz
        volume                  volume between 0.0 and 1.0
    '''
    # numpy.arange( [start,] stop, [step,] ) : return evenly spaced values
    # within a given interval.
    durations = arange( samplingRateInHz * durationInSec )
    samples = sin( 2 * pi * durations * freqInHz / samplingRateInHz )
    samples = samples * volume

    # float32 is 4 bytes. If float32 is passed to steam.write(), the byte count
    # (duration) is divided by 4. So we need to use tobytes to avoid this
    # dividing by 4.
    return samples.astype( float32 )

def generatePauses( samplingRateInHz, durationInSec ):
    pause = zeros( int( samplingRateInHz * durationInSec ) )
    return pause.astype( float32 )

def callback( in_data, frame_count, time_info, status ):
	global data
	out = data[ :frame_count ]
	data = data[ frame_count: ]
	return ( out * volume, paContinue )

volume = 0.5
samplingRateInHz = 44100
freqInHz = 440.0
toneDurationInSec = float( 1.0 )
pauseDurationInSec = float( 0.5 )
count = int( 2 )

tone = generateSamples( samplingRateInHz, toneDurationInSec, freqInHz, volume )
pause = generatePauses( samplingRateInHz, pauseDurationInSec )
# add pause to samples
samples = concatenate( ( tone, pause ) )
# repeat samples
data = array( [] ).astype( float32 )
for i in range( count ):
	data = concatenate( ( data , samples ) )

p = PyAudio()
stream = p.open( format=paFloat32, channels=1, rate=samplingRateInHz, output=True,
				 stream_callback=callback )
stream.start_stream()
while stream.is_active():
	time.sleep( 0.1 )
stream.stop_stream()
stream.close()
p.terminate()
