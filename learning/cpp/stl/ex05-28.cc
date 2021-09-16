#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    vector<int> v1( 5 );

    for( int i = 0 ; i < 5 ; ++i ) {
        v1[ i ] = i;
    }
    random_shuffle( v1.begin(), v1.end() );

    vector<int>::iterator k = max_element( v1.begin(), v1.end() );
    assert( *k == 4 );

    k = min_element( v1.begin(), v1.end() );
    assert( *k == 0 );

    return 0;
}
