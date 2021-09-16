#include <algorithm>
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
    set<char> s1;
    list<char>::iterator i;
    for( i = l1.begin() ; i != l1.end() ; ++i ) {
        s1.insert( *i );
    }

    list<char> l2;
    set<char>::iterator k;
    for( k = s1.begin() ; k != s1.end() ; ++k ) {
        l2.push_back( *k );
    }

    assert( l2 == make< list<char> >( " ATacdehilmnorstvy" ) );
    return 0;
}
