#include <cassert>
#include <cstring>
#include <list>
#include <set>
using namespace std;

template< typename Container >
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    list<char> l1 = make< list<char> >( "There is no distictly native "
                                        "American criminal class" );
    multiset<char> ms1;
    list<char>::iterator i;
    for( i = l1.begin() ; i != l1.end() ; ++i ) {
        ms1.insert( *i );
    }

    list<char> l2;
    multiset<char>::iterator k;
    for( k = ms1.begin() ; k != ms1.end() ; ++k ) {
        l2.push_back( *k );
    }

    assert( l2 == make< list<char> >( "       ATaaaaccccdeeeehiiiiiii"
                                      "lllmmnnnnnorrrsssstttvy" ) );
    return 0;
}
