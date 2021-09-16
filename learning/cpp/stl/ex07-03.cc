#include <cassert>
#include <cstring>
#include <functional>
#include <iostream>
#include <list>
#include <set>
#include <string>
using namespace std;

template< typename Container >
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

template< typename Container >
string make_string( const Container &c ) {
    string s;
    copy( c.begin(), c.end(), inserter( s, s.end() ) );
    return s;
}

int main() {
    list<char> l1 = make< list<char> >( "There is no distictly native "
                                        "American criminal class" );
    multiset<char> ms1;
    copy( l1.begin(), l1.end(), inserter( ms1, ms1.end() ) );
    assert( make_string( ms1 ) ==
            "       ATaaaaccccdeeeehiiiiiiilllmmnnnnorrrsssstttvy" );
    ms1.erase( 'a' );
    assert( make_string( ms1 ) ==
            "       ATccccdeeeehiiiiiiilllmmnnnnorrrsssstttvy" );

    multiset<char>::iterator i = ms1.find( 'e' );
    ms1.erase( i );
    assert( make_string( ms1 ) ==
            "       ATccccdeeehiiiiiiilllmmnnnnorrrsssstttvy" );

    return 0;
}
