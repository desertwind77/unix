#include <algorithm>
#include <cassert>
#include <deque>
#include <functional>
#include <string>
using namespace std;

int main() {
    deque<string> player( 5 );
    player[ 0 ] = "Pele";
    player[ 1 ] = "Platini";
    player[ 2 ] = "Maradona";
    player[ 3 ] = "Maradona";
    player[ 4 ] = "Rossi";

    deque<string>::iterator i = adjacent_find( player.begin(), player.end() );
    assert( ( *i == "Maradona" ) && *( i + 1 ) == "Maradona" );

    // Find the first name that is lexicographically greater
    // than the following name.
    deque<string>::iterator j = adjacent_find( player.begin(), player.end(),
                                               greater<string>() );
    assert( ( *j == "Platini" ) && *( j + 1 ) == "Maradona" );

    return 0;
}
