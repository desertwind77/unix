#include <execinfo.h>
#include <stdlib.h>
#include <stdio.h>

#define BUFFER_SIZE 1024

void printBacktrace( void ) { 
    int j, nptrs;
    void * buffer[ BUFFER_SIZE ];
    char ** strings;

    nptrs = backtrace( buffer, BUFFER_SIZE );
    printf( "backtrace() return %d addresses\n", nptrs );

    // backtrace_symbols_fd( buffer, nptrs, STDOUT_FILENO )
    // will do the same thing to the following.
    strings = backtrace_symbols( buffer, nptrs );
    if( strings == NULL ) { 
        perror( "backtrace_symbols" );
        exit( EXIT_FAILURE );
    }   

    for( j=0; j<nptrs; j++ ) { 
        printf( "%s\n", strings[ j ] );
    }   

    free( strings );
}

void test_print_backtrace( int ncalls ) { 
    if( ncalls > 1 ) { 
        test_print_backtrace( ncalls - 1 );
    } else {
        fprintf( stdout, "\n----- %s -----\n", __FUNCTION__ );
        printBacktrace();
    }   
}

int main() {
	test_print_backtrace( 10 );
}
