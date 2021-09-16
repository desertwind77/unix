#include <cassert>
#include <functional>
#include <numeric>
#include <vector>
using namespace std;

int main() {
    int x[ 20 ];

    for( int i = 0 ; i < 20 ; ++i ) {
        x[ i ] = i;
    }

    // 5 + 0 + 1 + 2 + ... + 12 = 195
    int result = accumulate( &x[ 0 ], &x[ 20 ], 5 );
    assert( result == 195 );

    // 10 * 1 * 2 * 3 * 4 = 240
    result = accumulate( &x[ 1 ], &x[ 5 ], 10, multiplies<int>() );
    assert( result == 240 );

    return 0;
}
