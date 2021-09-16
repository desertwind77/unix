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
    int N = 10000;
    vector<U> v1, v2;
    int k;

    for( k = 0 ; k != N ; ++k ) {
        vector<U>::size_type cap = v1.capacity();
        v1.push_back( U( k ) );
        if( v1.capacity() != cap ) {
            cout << "k: " << k << ", new capacity: " << v1.capacity() << endl;
        }
    }

    v2.reserve( N );
    for( k = 0 ; k != N ; ++k ) {
        vector<U>::size_type cap = v2.capacity();
        v2.push_back( U( k ) );
        if( v2.capacity() != cap ) {
            cout << "k: " << k << ", new capacity: " << v2.capacity() << endl;
        }
    }

    return 0;
}
