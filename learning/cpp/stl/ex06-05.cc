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
    vector<char> v1 = make< vector<char> >( "Bjarne Stroustrup" );
    vector<char> v2;
    vector<char>::iterator i;

    for( i = v1.begin() ; i != v1.end() ; ++i ) {
        v2.push_back( *i );
    }
    assert( v1 == v2 );

    v1 = make< vector<char> >( "Bjarne Stroustrup" );
    v2 = make< vector<char> >( "" );

    for( i = v1.begin() ; i != v1.end() ; ++i ) {
        v2.insert( v2.begin(), *i );
    }
    assert( v2 == make< vector<char> >( "purtsuortS enrajB" ) );

    reverse( v1.begin(), v1.end() );
    assert( v2 == v1 );

    return 0;
}
