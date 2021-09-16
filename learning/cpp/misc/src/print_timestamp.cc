#include <stdarg.h>		// For va_start, va_end
#include <sys/time.h>	// For struct timeval, struct tm, gettimeofday
#include <stdio.h>		// For printf, snprintf
#include <string.h>		// For memset
#include <time.h>		// For localtime_r, strftime

#define BUFFER_SIZE 1024

int printTimestamp( const char * format, ... ) { 
    char buffer[ 1024 ];
    va_list args;
    struct timeval tv; 
    struct tm tval;
    unsigned int offset;

    // We need to do this because stack may not be 0.
    memset( buffer, 0, BUFFER_SIZE );

    // Print timestamp into the buffer
    gettimeofday( &tv, NULL );
    localtime_r( ( time_t * ) &tv.tv_sec, &tval );
    offset = strftime( buffer, BUFFER_SIZE, "%F %T", &tval );
    offset += snprintf( buffer + offset, BUFFER_SIZE - offset,
                        ".%06lu ", tv.tv_usec );

    // Print format and arguments into the buffer
    va_start( args, format );
    offset = vsnprintf( buffer + offset, BUFFER_SIZE - offset, format, args );
    va_end( args );

    // Print the buffer
    printf( "%s", buffer );
    return offset;
}

int main() {
	printTimestamp( "This is my message num = %d, string = %s float = %f\n",
					210, "test string", 30.1 );
	return 0;
}
