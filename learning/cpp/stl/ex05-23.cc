#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

int main() {
    vector<int> v = { 25, 7, 9, 2, 0, 5, 21 };
    const int N = 4;

    nth_element( v.begin(), v.begin() + N, v.end() );

    int i;
    for( i = 0 ; i < N ; ++i ) {
        assert( v[ N ] >= v[ i ] );
    }

    for( i = N + 1 ; i < 7 ; ++i ) {
        assert( v[ N ] <= v[ i ] );
    }

    return 0;
}
