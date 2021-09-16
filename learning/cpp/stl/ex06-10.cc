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
    list<char> l1 = make< list<char> >( "Bjarne Stroustrup" );
    list<char> l2;
    list<char>::iterator i;

    for( i = l1.begin() ; i != l1.end() ; ++i ) {
        l2.push_back( *i );
    }
    assert( l1 == l2 );

    l1 = make< list<char> >( "Bjarne Stroustrup" );
    l2 = make< list<char> >( "" );

    for( i = l1.begin() ; i != l1.end() ; ++i ) {
        l2.insert( l2.begin(), *i );
    }
    assert( l2 == make< list<char> >( "purtsuortS enrajB" ) );

    reverse( l1.begin(), l1.end() );
    assert( l2 == l1 );

    return 0;
}
