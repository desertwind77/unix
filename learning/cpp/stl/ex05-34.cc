#include <iostream>
#include <iterator>
#include <numeric>
using namespace std;

int main() {
    const int N = 5;
    int x1[ N ], x2[ N ];

    for( int i = 0 ; i < N ; ++i ) {
        x1[ i ] = i + 1;
        x2[ i ] = i + 2;
    }

    int result = inner_product( &x1[ 0 ], &x1[ N ], &x2[ 0 ], 0 );
    cout << "inner product = " << result << endl;

    result = inner_product( &x1[ 0 ], &x1[ N ], &x2[ 0 ], 1,
                            multiplies<int>(), plus<int>() );
    cout << "inner product (swap + and *) = " << result << endl;

    return 0;
}
