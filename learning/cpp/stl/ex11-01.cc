#include <iostream>
#include <cassert>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;

class U : public binary_function<U, U, bool> {
 public:
    int id;
    bool operator()( const U &x, const U &y) const {
        return x.id >= y.id;
    }
    friend ostream& operator<<( ostream &o, const U &x ) {
        o << x.id;
        return o;
    }
};

int main() {
    vector<U> v1( 1000 );
    for( int i = 0 ; i != 1000 ; ++i )
        v1[ i ].id = 1000 - i - 1;
    sort( v1.begin(), v1.end(), not2( U() ) );
    for( int k = 0 ; k != 1000 ; ++k )
        assert( v1[ k ].id == k );
    return 0;
}
