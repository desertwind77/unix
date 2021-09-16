#!/usr/bin/python3

class Clock( object ):
    def __init__( self, hours, minutes, seconds ):
        self.set_Clock( hours, minutes, seconds )

    def set_Clock( self, hours, minutes, seconds ):
        if type( hours ) == int and 0 <= hours and hours < 24:
            self._hours = hours
        else:
            raise TypeEror( "Hours have to be integers between 0 and 23!" )

        if type( minutes ) == int and 0 <= minutes and minutes < 60:
            self._minutes = minutes 
        else:
            raise TypeEror( "Minutes have to be integers between 0 and 59!" )

        if type( seconds ) == int and 0 <= seconds and seconds < 60:
            self._seconds = seconds
        else:
            raise TypeEror( "Minutes have to be integers between 0 and 59!" )

    def __str__( self ):
        return "{0:02d}:{1:02d}:{2:02d}".format( self._hours, self._minutes,
                                                 self._seconds )

    def tick( self ):
        if self._seconds == 59:
            self._seconds = 0
            if self._minutes == 59:
                self._minutes = 0
                if self._hours == 23:
                    self._hours = 0
                else:
                    self._hours +=1
            else:
                self._minutes += 1
        else:
            self._seconds += 1

if __name__ == "__main__":
    x = Clock( 23, 59, 59 )
    print( x )
    x.tick()
    print( x )
    y = str( x )
    print( type( y ) )
