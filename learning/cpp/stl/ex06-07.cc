#include <cstring>
#include <iostream>
#include <vector>
using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    vector<char> v1 = make< vector<char> >( "abcdefghij" );

    while( v1.size() > 0 ) {
        cout << v1.back();
        v1.pop_back();
    }
    cout << endl;

    return 0;
}
