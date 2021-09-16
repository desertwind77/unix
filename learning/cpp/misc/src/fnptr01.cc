#include <stdio.h>

void normal_function( int param ) {
    printf( "param = %d\n", param );
}
 
int main()
{
	// Declaration and assigment
    void (*fnPtr1)( int ) = &normal_function;
    void (*fnPtr2)( int ) = normal_function;
 
	// Derefence
    (*fnPtr1)( 10 );
    fnPtr2( 20 );

    return 0;
}
