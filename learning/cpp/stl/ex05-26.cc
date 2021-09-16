#include <algorithm>
#include <cassert>
#include <string>
#include <vector>
using namespace std;

template <typename Container>
Container make( string s ) {
    return Container( s.begin(), s.end() );
}

int main() {
    bool result;
    vector<char> v1 = make< vector<char> >( "abcde" );
    vector<char> v2 = make< vector<char> >( "aeiou" );

    result = includes( v1.begin(), v1.end(), v2.begin(), v2.end() );
    assert( !result );

    result = includes( v1.begin(), v1.end(), v2.begin(), v2.begin() + 2 );
    assert( result );
    
    vector<char> setUnion;
    set_union( v1.begin(), v1.end(), v2.begin(), v2.end(),
              back_inserter( setUnion ) );
    assert( setUnion == make< vector<char> >( "abcdeiou" ) );

    vector<char> setIntersect;
    set_intersection( v1.begin(), v1.end(), v2.begin(), v2.end(),
              back_inserter( setIntersect ) );
    assert( setIntersect == make< vector<char> >( "ae" ) );

    vector<char> setDifference;
    set_symmetric_difference( v1.begin(), v1.end(), v2.begin(), v2.end(),
              back_inserter( setDifference ) );
    assert( setDifference == make< vector<char> >( "bcdiou" ) );

    return 0;
}
