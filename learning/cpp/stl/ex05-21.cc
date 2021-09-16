#include <algorithm>
#include <cassert>
#include <iostream>
#include <iterator>
#include <vector>
using namespace std;

int main() {
    const int N = 11;
    int a1[ N ] = { 1, 2, 0, 3, 3, 0, 7, 7, 7, 0, 8 };
    vector<int> v1;

    for( int i = 0 ; i < N ; ++i ) {
        v1.push_back( a1[ i ] );
    }

    vector<int>::iterator new_end = unique( v1.begin(), v1.end() );
    assert( v1.size() == N );
    v1.erase( new_end, v1.end() );

    copy( v1.begin(), v1.end(), ostream_iterator<int>( cout, " " ) );
    cout << endl;

    return 0;
}
