#include <iostream>
#include <cassert>
#include <vector>
using namespace std;

class multiply {
 public:
    int operator()( int x, int y ) const { return x * y; }
};

multiply multfunobj;

int multfun( int x, int y ) { return x * y; }

template <typename InputIterator, typename T>
T accumulate1( InputIterator first, InputIterator last, T init,
              T (*binary_function)( T x, T y ) ) {
    while( first != last ) {
        init =(*binary_function)( init, *first );
        ++first;
    }
    return init;
}

int main() {
    int x[ 5 ] = { 2, 3, 5, 7, 11 };
    vector<int> v1( &x[ 0], &x[ 5 ] );
    int product = accumulate1( v1.begin(), v1.end(), 1, &multfun );
    assert( product == 2310 );
    return 0;
}
