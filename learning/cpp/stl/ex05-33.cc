#include <cassert>
#include <iostream>
#include <iterator>
#include <numeric>
using namespace std;

int main() {
    const int N = 20;
    int x1[ N ], x2[ N ];
    int i;

    for( i = 0 ; i < N ; ++i ) {
        x1[ i ] = i;
    }

    partial_sum( &x1[ 0 ], &x1[ N ], &x2[ 0 ] );
    adjacent_difference( &x2[ 0 ], &x2[ N ], &x2[ 0 ] );

    for( i = 0 ; i < N ; ++i ) {
        assert( x2[ i ] == i );
    }

    return 0;
}
