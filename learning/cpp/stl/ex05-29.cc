#include <algorithm>
#include <cassert>
#include <cstring>
#include <vector>
using namespace std;

template< typename Container >
Container make( const char s[] ) {
    return Container( s[ 0 ], s[ strlen( s ) ] );
}

int main() {
    vector<char> v1 = make< vector<char> >( "hello" );
    vector<char> v2 = make< vector<char> >( "hello" );

    bool result = lexicographical_compare( v1.begin(), v1.end(), v2.begin(), v2.end() );
    assert( result = true );

    return 0;
}
