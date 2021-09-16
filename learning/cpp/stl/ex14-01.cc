#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <list>
#include <map>
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

typedef vector<PS>::const_iterator PSi;
typedef pair<PSi, PSi> PPS;

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

    typedef map<int, list<PPS>, greater<int> > map_1;
    map_1 groups;

    // Find anagram groups
    PSi j = word_pairs.begin(), finis = word_pairs.end(), k;
    while( true ) {
        j = adjacent_find( j, finis, firstEqual );
        if( j == finis ) break;
        k = find_if( j + 1, finis, not1( bind1st( firstEqual, *j ) ) );
        if( k - j > 1 ) {
            groups[ k - j ].push_back( PPS( j, k ) );
        }
        j = k;
    }

    // Output the anagram groups
    map_1::const_iterator m;
    for( m = groups.begin() ; m != groups.end() ; ++m ) {
        cout << "Anagram groups of size " << m->first << endl;
        list<PPS>::const_iterator l;
        for( l = m->second.begin() ; l != m->second.end() ; ++l ) {
            cout << "   ";
            j = l->first;
            k = l->second;
            copy( j, k, ostream_iterator<string>( cout, " " ) );
            cout << endl;
        }
    }

    return 0;
}
