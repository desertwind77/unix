#include <algorithm>
#include <cassert>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s ("abcdefghijklmnopqrstuvwxyz" );
    vector<char> v1( s.begin(), s.end() );
    vector<char> v2( v1.size() );

    copy( v1.begin(), v1.end(), v2.begin() );
    assert( v1 == v2 );

    // shift left by 4 position
    copy( v1.begin() + 4, v1.end(), v1.begin() );
    assert( string( v1.begin(), v1.end() ) == string( "efghijklmnopqrstuvwxyzwxyz" ) );

    // shift right by 2 position
    copy_backward( v1.begin(), v1.end() - 2, v1.end() );
    assert( string( v1.begin(), v1.end() ) == string( "efefghijklmnopqrstuvwxyzwx" ) );

    return 0;
}
