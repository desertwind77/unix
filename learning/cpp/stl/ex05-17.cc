#include <algorithm>
#include <cassert>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s( "Software Engineering " );
    vector<char> v1( s.begin(), s.end() );

    rotate( v1.begin(), v1.begin() + 9, v1.end() );
    assert( string( v1.begin(), v1.end() ) == string( "Engineering Software " ) );

    return 0;
}
