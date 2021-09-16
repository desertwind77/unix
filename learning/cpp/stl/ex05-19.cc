#include <algorithm>
#include <cassert>
#include <cstring>
#include <vector>
using namespace std;

template < typename Container >
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    vector<char> v1 = make< vector<char> >( "HELLO" );
    vector<char> v2 = make< vector<char> >( "THERE" );
    vector<char> tmp1 = v1;
    vector<char> tmp2 = v2;

    swap_ranges( v1.begin(), v1.end(), v2.begin() );
    assert( v1 == tmp2 && v2 == tmp1 );

    return 0;
}
