#include <algorithm>
#include <cassert>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s( "Hello there" );
    vector<char> v1( s.begin(), s.end() );

    fill( v1.begin(), v1.begin() + 5, 'X' );
    assert( string( v1.begin(), v1.end() ) == string( "XXXXX there" ) );

    fill_n( v1.begin() + 5, 3, 'Y' );
    assert( string( v1.begin(), v1.end() ) == string( "XXXXXYYYere" ) );

    return 0;
}
