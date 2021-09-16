#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>
using namespace std;

struct PS : pair<string, string> {
    PS() : pair<string, string>( string(), string() ) {}
    PS( const string &s ) : pair<string, string>( s, s ) {
        sort( first.begin(), first.end() );
    }
    operator string() const { return second; }
};

struct FirstLess: binary_function<PS, PS, bool> {
    bool operator()( const PS &p, const PS &q ) const {
        return p.first < q.first;
    }
} firstLess;

struct FirstEqual : binary_function<PS, PS, bool> {
    bool operator()( const PS &p, const PS &q ) const {
        return p.first == q.first;
    }
} firstEqual;

int main() {
    string dictionary_name( "diction" );
    ifstream ifs( dictionary_name.c_str() );
    if( !ifs.is_open() ) {
        cout << "Unable to open " << dictionary_name << endl;
        exit( 1 );
    }

    typedef istream_iterator<string> string_input;
    vector<PS> word_pairs;
    copy( string_input( ifs ), string_input(), back_inserter( word_pairs ) );

    sort( word_pairs.begin(), word_pairs.end(), firstLess );

    vector<PS>::const_iterator j = word_pairs.begin(),
                               finis = word_pairs.end(), k;
    while( true ) {
        // Searches the range [first, last) for two consecutive identical elements.
        j = adjacent_find( j, finis, firstEqual );
        if( j == finis ) break;
        k = find_if( j + 1, finis, not1( bind1st( firstEqual, *j ) ) );
        cout << " ";
        copy( j, k, ostream_iterator<string>( cout, " " ) );
        cout << endl;
        j = k;
    }

    return 0;
}
