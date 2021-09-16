#include <algorithm>
#include <cassert>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s( "FERRARI" );
    vector<char> v1( s.begin(), s.end() );

    replace( v1.begin(), v1.end(), 'R', 'S' );
    assert( string( v1.begin(), v1.end() ) == string( "FESSASI" ) );

    return 0;
}
