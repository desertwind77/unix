#include <algorithm>
#include <cassert>
#include <iostream>
#include <iterator>
#include <vector>
using namespace std;

int sum( int x, int y ) { return x + y; }

int main() {
    int a1[ 5 ] = { 0, 1, 2, 3, 4 };
    int a2[ 5 ] = { 6, 7, 8, 9, 10 };
    ostream_iterator<int> out( cout, " " );

    transform( &a1[ 0 ], &a1[ 5 ], &a2[ 0 ], out, sum );
    cout << endl;

    return 0;
}
