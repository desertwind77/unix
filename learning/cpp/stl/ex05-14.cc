#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>
using namespace std;

int main() {
    const int N = 20;
    vector<int> v1( N );

    for( int i = 0 ; i < N ; ++i ) {
        v1[ i ] = i;
    }

    for( int j = 0 ; j < 3 ; ++j ) {
        random_shuffle( v1.begin(), v1.end() );
        copy( v1.begin(), v1.end(), ostream_iterator<int>( cout, " " ) );
        cout << endl;
    }

    return 0;
}
