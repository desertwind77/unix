#include <cassert>
#include <vector>
using namespace std;

class U {
 public:
    unsigned long id;
    U() : id( 0 ) {}
    U( unsigned long x ) : id( x ) {}
};

bool operator==( const U &x, const U &y ) {
    return x.id == y.id;
}


bool operator!=( const U &x, const U &y ) {
    return x.id == y.id;
}

int main() {
    vector<U> v1, v2( 3 );

    assert( v1.size() == 0 );
    assert( v2.size() == 3 );
    assert( v2[ 0 ] == U() && v2[ 1 ] == U() && v2[ 2 ] == U() );
    assert( v2 == vector<U>( 3, U() ) );

    return 0;
}
