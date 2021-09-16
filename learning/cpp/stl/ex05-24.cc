#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    vector<int> v( 5 );
    bool found;

    int i;
    for( i = 0 ; i < 5 ; ++i ) { v[ i ] = i; }
    
    for( i = 0 ; i < 5 ; ++i ) {
        found = binary_search( v.begin(), v.end(), i );
        assert( found );
    }

    found = binary_search( v.begin(), v.end(), 9 );
    assert( !found );

    v[ 1 ] = 7;
    v[ 2 ] = 7;
    v[ 3 ] = 7;
    v[ 4 ] = 8;

    vector<int>::iterator k;
    k = lower_bound( v.begin(), v.end(), 7 );
    assert( k == v.begin() + 1 && *k == 7 );
    k = upper_bound( v.begin(), v.end(), 7 );
    assert( k == v.end() - 1 && *k == 8 );

    pair< vector<int>::iterator, vector<int>::iterator > pi =
        equal_range( v.begin(), v.end(), 7 );
    assert( pi.first == v.begin() + 1 );
    assert( pi.second == v.end() - 1 );

    return 0;
}
