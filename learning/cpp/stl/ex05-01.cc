#include <algorithm>
#include <cassert>
#include <iostream>
using namespace std;

int main() {
    int a[ 1000 ];
    int i;

    for( i = 0 ; i < 1000 ; ++i ) {
        a[ i ] = 1000 - i - 1;
    }

    sort( &a[ 0 ], &a[ 1000 ] );

    for( i = 0 ; i < 1000 ; ++i ) {
        assert( a[ i ] == i );
    }

    return 0;
}
