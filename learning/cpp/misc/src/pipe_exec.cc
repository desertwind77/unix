#include <assert.h>     // For assert
#include <stdio.h>      // For File, popen, fread, pclose
#include <string.h>     // For memset
#include <stdlib.h>     // For system

#define BUFSIZE 1024

/*
 * execExternalCmd : execute an external command and store
 *  the output in the buffer
 * return value : 0 on success; otherwise 0
 */
int execExternalCmd( const char *cmd,char *buffer,
                     int bufSize ) { 
   FILE *fp;
   int ret = 0;

   if ( ( fp = popen( cmd, "r" ) ) == NULL ) {
      perror( "popen" );
      return -1; 
   }   

   fread( buffer, sizeof( char ), bufSize, fp);
   if ( ferror( fp ) != 0 ) {
       fprintf( stderr, "unable to read from pipe\n" );
       // I don't care about the return value of pclose
       // cause I will return error( -1 ) because of
       // fread failure anyway.
       pclose( fp );
       return -1;
   }

   if ( ( ret = pclose( fp ) ) == -1 ) {
      perror( "pclose" );
      return -1;
   }   

   return 0;
}

int main(void) {
    const char *cmd = "ls | sort";
    char buffer[ BUFSIZE ];
    
    memset( buffer, 0, BUFSIZE );
    assert( execExternalCmd( cmd, buffer, BUFSIZE ) == 0 );
    fprintf( stdout, "%s\n", buffer );

   return 0;
}
