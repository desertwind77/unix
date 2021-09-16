#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    vector<int> v1( 5 );
    vector<int> v2( 5 );
    vector<int> v3( 10 );

    int i;
    for( i = 0 ; i < 5 ; ++i ) {
        v1[ i ] = 2 * i;
        v2[ i ] = 1 + 2 * i;
    }

    merge( v1.begin(), v1.end(), v2.begin(), v2.end(),
            v3.begin() );
    for( i = 0 ; i < 10 ; ++i ) {
        assert( v3[ i ] == i );
    }

    for( i = 0 ; i < 5 ; ++i ) {
        v3[ i ] = v1[ i ];
        v3[ i + 5 ] = v2[ i ];
    }

    inplace_merge( v3.begin(), v3.begin() + 5, v3.end() );
    for( i = 0 ; i < 10 ; ++i ) {
        assert( v3[ i ] == i );
    }

    return 0;
}
