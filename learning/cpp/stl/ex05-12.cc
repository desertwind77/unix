#include <algorithm>
#include <cassert>
#include <string>
#include <vector>
using namespace std;

template< typename T >
class calc_square {
    T i;
 public:
    calc_square() : i( 0 ) {}
    T operator()() { ++i; return i * i; }
};

int main() {
    vector<int> v1( 10 );

    generate( v1.begin(), v1.end(), calc_square<int>() );
    for( int i = 0 ; i < 10 ; ++i ) {
        assert( v1[ i ] == ( i + 1 ) * ( i + 1 ) );
    }

    return 0;
}
