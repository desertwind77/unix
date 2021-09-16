#include <stdio.h>

float add( float a, float b ) {
	return a + b;
}

float sub( float a, float b) {
	return a - b;
}

float mul( float a, float b) {
	return a * b;
}

float div( float a, float b ) {
	return a / b;
}

int main() {
	int i;
    float (*fnPtrArray[])( float, float ) =
        { add, sub, mul, div};
 
	for ( i = 0 ; i < 4 ; i ++ )
        printf( "Result of function %d = %.2f\n",
                i, (*fnPtrArray[ i ])( 10, 2 ) );
 
    return 0;
}
