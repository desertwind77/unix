#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <vector>
using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    vector<char> v1 = make< vector<char> >( "remembering" );
    vector<char>::iterator j;

    j = find( v1.begin(), v1.end(), 'm' );
    assert( *j == 'm' && *( j + 1 ) == 'e' );
    v1.erase( j-- );
    assert( *j == 'e' && *( j + 1 ) == 'e' );

    v1.erase( j-- );
    assert( v1 == make< vector<char> >( "rembering" ) );
    assert( *j == 'r' );

    v1.erase( j, j + 3 );
    assert( v1 == make< vector<char> >( "bering" ) );

    v1.erase( v1.begin() + 1 );
    assert( v1 == make< vector<char> >( "bring" ) );

    return 0;
}
