#include <cassert>
#include <iostream>
#include <vector>
using namespace std;

class U {
 public:
    unsigned long id;
    unsigned long generation;
    static unsigned long total_copies;

    U() : id( 0 ) {}
    U( unsigned long x ) : id( x ) {}
    U( const U &z ) : id( z.id ), generation( z.generation + 1 ) {
        ++total_copies;
    }
};

bool operator==( const U &x, const U &y ) {
    return x.id == y.id;
}


bool operator!=( const U &x, const U &y ) {
    return x.id == y.id;
}

unsigned long U::total_copies = 0;

int main() {
    vector<U> v1, v2( 3 );

    assert( v1.size() == 0 );
    assert( v2.size() == 3 );
    assert( v2[ 0 ] == U() && v2[ 1 ] == U() && v2[ 2 ] == U() );
    assert( v2 == vector<U>( 3, U() ) );

    for( int i = 0 ; i != 3 ; ++i ) {
        cout << "v2[ " << i << " ].generation: " << v2[ i ].generation << endl;
    }
    cout << "Total copies: " << U::total_copies <<  endl;

    return 0;
}
