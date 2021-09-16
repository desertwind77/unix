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
    list<char> l2 = make< list<char> >( "except Congress. - Mark Twain" );

    multiset<char> ms1;
    copy( l1.begin(), l1.end(), inserter( ms1, ms1.end() ) );
    assert( make_string( ms1 ) ==
            "       ATaaaaccccdeeeehiiiiiiilllmmnnnnorrrsssstttvy" );

    multiset<char>::iterator i = ms1.lower_bound( 'c' );
    multiset<char>::iterator j = ms1.upper_bound( 'r' );
    ms1.erase( i, j ); 
    assert( make_string( ms1 ) ==
            "       ATaaaasssstttvy" );

    list<char> found, not_found;
    list<char>::iterator k;
    for( k = l2.begin() ; k != l2.end() ; ++k ) {
        if( ms1.find( *k ) != ms1.end() ) {
            found.push_back( *k );
        } else {
            not_found.push_back( *k );
        }
    }
    assert( found == make< list<char> >( "t ss  a Ta" ) );
    assert( not_found == make< list<char> >( "excepCongre.-Mrkwin" ) );

    return 0;
}
