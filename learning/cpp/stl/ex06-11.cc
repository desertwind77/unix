#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <list>
using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    list<char> l1 = make< list<char> >( "remembering" );
    list<char>::iterator j;

    j = find( l1.begin(), l1.end(), 'i' );
    l1.erase( j++ );
    assert( l1 == make< list<char> >( "rememberng" ) );

    l1.erase( j++ );
    assert( l1 == make< list<char> >( "rememberg" ) );

    l1.erase( j++ );
    assert( l1 == make< list<char> >( "remember" ) );

    l1.erase( l1.begin() );
    assert( l1 == make< list<char> >( "emember" ) );

    l1.erase( l1.begin() );
    assert( l1 == make< list<char> >( "member" ) );

    return 0;
}
