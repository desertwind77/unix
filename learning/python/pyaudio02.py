#!/usr/bin/env python3
from pyaudio import PyAudio, paFloat32
from numpy import sin, float32, arange, pi

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
    return samples.astype( float32 ).tobytes()

volume = 0.5
samplingRateInHz = 44100
durationInSec = 1.0
freqInHz = 440.0
samples = generateSamples( samplingRateInHz, durationInSec, freqInHz, volume )
p = PyAudio()
# For paFloat32, sample values must be in range [ -1.0, 1.0 ]
stream = p.open( format=paFloat32, channels=1, rate=samplingRateInHz, output=True)
stream.write( samples )
stream.stop_stream()
stream.close()
p.terminate()
