#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <deque>
using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    deque<char> dq1 = make< deque<char> >( "Bjarne Stroustrup" );
    deque<char> dq2;
    deque<char>::iterator i;

    for( i = dq1.begin() ; i != dq1.end() ; ++i ) {
        dq2.push_back( *i );
    }
    assert( dq1 == dq2 );

    dq1 = make< deque<char> >( "Bjarne Stroustrup" );
    dq2 = make< deque<char> >( "" );

    for( i = dq1.begin() ; i != dq1.end() ; ++i ) {
        dq2.insert( dq2.begin(), *i );
    }
    assert( dq2 == make< deque<char> >( "purtsuortS enrajB" ) );

    reverse( dq1.begin(), dq1.end() );
    assert( dq2 == dq1 );

    return 0;
}
