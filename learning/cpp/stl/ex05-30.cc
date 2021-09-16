#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    vector<int> v1( 3 );

    for( int i = 0 ; i < 3 ; ++i ) {
        v1[ i ] = i;
    }

    // In lexicographical order the permutaions of 0 1 2 are
    // 0 1 2, 0 2 1, 1 0 2, 1 2 0, 2 0 1, 2 1 0
    next_permutation( v1.begin(), v1.end() );
    assert( ( v1[ 0 ] == 0 ) && ( v1[ 1 ] == 2 ) && ( v1[ 2 ] == 1 ) );

    prev_permutation( v1.begin(), v1.end() );
    assert( ( v1[ 0 ] == 0 ) && ( v1[ 1 ] == 1 ) && ( v1[ 2 ] == 2 ) );

    return 0;
}
