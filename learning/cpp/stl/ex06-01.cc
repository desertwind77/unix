#include <cassert>
#include <vector>
using namespace std;

int main() {
    vector<char> v1, v2( 3, 'x' );

    assert( v1.size() == 0 );
    assert( v2.size() == 3 );
    assert( v2[ 0 ] == 'x' && v2[ 1 ] == 'x'  && v2[ 2 ] == 'x' );
    assert( v2 == vector<char>( 3, 'x' ) &&
            v2 != vector<char>( 4, 'x' ) );

    return 0;
}
