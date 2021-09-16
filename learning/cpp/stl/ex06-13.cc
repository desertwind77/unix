#include <algorithm>
#include <cassert>
#include <cstring>
#include <list>
using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    list<char> l1 = make< list<char> >( "Stroustrup" );

    l1.sort();
    assert( l1 == make< list<char> >( "Soprrsttuu" ) );
    
    l1.unique();
    assert( l1 == make< list<char> >( "Soprstu" ) );

    return 0;
}
