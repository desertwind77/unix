#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    const int N = 11;
    int a1[ N ] = { 1, 2, 0, 3, 4, 0, 5, 6, 7, 0, 8 };
    vector<int> v1;
    int i;

    for( i = 0 ; i < N ; ++i ) {
        v1.push_back( a1[ i ] );
    }

    // Remove the zeros from v1
    vector<int>::iterator new_end;
    new_end = remove( v1.begin(), v1.end(), 0 );
    assert( v1.size() == N );

    // The nonrzero elements are left in [ v1.begin(), new_end ). Erase the rest.
    v1.erase( new_end, v1.end() );
    assert( v1.size() == N - 3 );
    for( i = 0 ; i < v1.size() ; ++i ) {
        assert( v1[ i ] == i + 1 );
    }

    return 0;
}
