#include <iostream>
#include <cassert>
#include <vector>
using namespace std;

class multiply {
 public:
    int operator()( int x, int y ) const { return x * y; }
};

multiply multfunobj;

template <typename InputIterator, typename T, typename BinaryFunction>
T accumulate1( InputIterator first, InputIterator last, T init,
              BinaryFunction binary_function ) {
    while( first != last ) {
        init =binary_function( init, *first );
        ++first;
    }
    return init;
}

int main() {
    int x[ 5 ] = { 2, 3, 5, 7, 11 };
    vector<int> v1( &x[ 0], &x[ 5 ] );
    int product = accumulate1( v1.begin(), v1.end(), 1, multfunobj );
    assert( product == 2310 );
    return 0;
}
