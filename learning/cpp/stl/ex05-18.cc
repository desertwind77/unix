#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    int high = 250, low = 0;
    swap( high, low );
    assert( high == 0 && low == 250 );

    vector<int> v1( 100, 1 ), v2( 200, 2 );
    swap( v1, v2 );
    assert( v1 == vector<int>( 200, 2 ) &&
            v2 == vector<int>( 100, 1 ) );

    return 0;
}
