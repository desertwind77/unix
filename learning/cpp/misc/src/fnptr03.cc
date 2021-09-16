#include <stdio.h>
#include <stdlib.h>
 
void print_int_array( int* data, int elem ) {
    int i;

    for( i=0; i<elem; i++ ) {
        printf( "%d ", *( (int*)data + i ) );
    }
}

int ascending_compare( const void * a, const void * b ) {
  return ( *( (int*)a ) - *( (int*)b ) );
}
 
int descending_compare( const void * a, const void * b ) {
  return ( *( (int*)b ) - *( (int*)a ) );
}
 
int main () {
    int data[] = { 99, 5, 47, 8, 13, 76, 11, 64 };
    int elem = sizeof( data )/ sizeof( data[ 0 ] );
    int i;

    qsort( data, elem, sizeof( int ), ascending_compare );
    printf( "Ascending order  : " );
    print_int_array( data, elem );
    printf( "\n" );

    qsort( data, elem, sizeof( int ), descending_compare );
    printf( "Descending order : " );
    print_int_array( data, elem );
    printf( "\n" );
    
    return 0;
}
