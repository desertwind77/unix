#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <list>
#include <map>
#include <string>
#include <vector>
using namespace std;

/*
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
*/
typedef multimap<string, string> multimap_1;
typedef multimap_1::value_type PS;
typedef multimap_1::const_iterator PSi;
typedef pair<PSi, PSi> PPS;
 
int main() {
    string dictionary_name( "diction" );
    ifstream ifs( dictionary_name.c_str() );
    if( !ifs.is_open() ) {
        cout << "Unable to open " << dictionary_name << endl;
        exit( 1 );
    }

    // Read dictionary into multimap
    typedef istream_iterator<string> string_input;
    multimap_1 word_pairs;
    for( string_input in( ifs ) ; in != string_input() ; ++in ) {
        string word = *in;
        sort( word.begin(), word.end() );
        word_pairs.insert( PS( word, *in ) );
    }

    // Find anagram groups
    typedef map<int, list<PPS>, greater<int> > map_1;
    map_1 groups;
    PSi j = word_pairs.begin(), finis = word_pairs.end(), k;

    while( true ) {
        j = adjacent_find( j, finis,
                           not2( word_pairs.value_comp() ) );
        if( j == finis ) break;

        k = find_if( j, finis, bind1st( word_pairs.value_comp(), *j ) );
        multimap_1::size_type n = distance( j, k );
        if( n > 1 ) {
            groups[ n ].push_back( PPS( j, k ) );
        }

        j = k;
    }

    // print output
    map_1::const_iterator m;
    for( m = groups.begin() ; m != groups.end() ; ++m ) {
        cout << "Anagram groups of size " << m->first << endl;
        list<PPS>::const_iterator l;
        for( l = m->second.begin() ; l != m->second.end() ; ++l ) {
            cout << "   ";
            j = l->first;
            k = l->second;
            for( ; j != k ; ++j ) {
                cout << j->second << " ";
            }
            cout << endl;
        }
    }

    return 0;
}
