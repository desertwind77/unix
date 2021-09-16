#include <iostream>
#include <iterator>
#include <numeric>
using namespace std;

int main() {
    const int N = 20;
    int x1[ N ], x2[ N ];
    int i;

    for( i = 0 ; i < N ; ++i ) {
        x1[ i ] = i;
    }

    partial_sum( &x1[ 0 ], &x1[ N ], &x2[ 0 ] );

    ostream_iterator<int> out( cout, " " );
    copy( &x2[ 0 ], &x2[ 20 ], out );
    cout << endl;

    return 0;
}
