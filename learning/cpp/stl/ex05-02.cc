#include <algorithm>
#include <cassert>
#include <iostream>
using namespace std;

int main() {
    int a[ 1000 ], b[ 1000 ];
    int i;

    for( i = 0 ; i < 1000 ; ++i ) {
        a[ i ] = i;
    }

    reverse_copy( &a[ 0 ], &a[ 1000 ], &b[ 0 ] );

    for( i = 0 ; i < 1000 ; ++i ) {
        assert( ( a[ i ] == i ) && ( b[ i ] == 1000 - i - 1 ) );
    }

    return 0;
}
