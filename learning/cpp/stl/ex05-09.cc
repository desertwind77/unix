#include <vector>
#include <deque>
#include <algorithm>
#include <cassert>
using namespace std;

int main() {
    vector<int> v1( 20 );
    deque<int> d1( 5 );
    int i;

    for( i = 0 ; i < 20 ; ++i ) {
        v1[ i ] = i;
    }
    for( i = 0 ; i < 5 ; ++i ) {
        d1[ i ] = i + 5;
    }

    vector<int>::iterator k =
        search( v1.begin(), v1.end(), d1.begin(), d1.end() );

    for( i = 0 ; i < 5 ; ++i ) {
        assert( *( k + i ) == i + 5 );
    }

    return 0;
}
