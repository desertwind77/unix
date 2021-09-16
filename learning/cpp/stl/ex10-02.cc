#include <algorithm>
#include <cstring>
#include <iostream>
#include <iterator>
#include <vector>
using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    vector<char> v1 = make< vector<char> >( "now is the time" );
    ostream_iterator<char> out( cout, "" );

    copy( v1.begin() , v1.end(), out );
    cout << endl;

    vector<char>::iterator i = find( v1.begin(), v1.end(), 't' );
    copy( i, v1.end(), out );
    cout << endl;

    vector<char>::reverse_iterator r = find( v1.rbegin(), v1.rend(), 't' );
    copy( r, v1.rend(), out );
    cout << endl;

    copy( r.base() - 1, v1.end(), out );
    cout << endl;

    return 0;
}
