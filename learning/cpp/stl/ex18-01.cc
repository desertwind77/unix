#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <iomanip>
#include <map>
#include <set>
using namespace std;

typedef map<string, string> data_map;

struct earlier : binary_function<string, string, bool> {
    bool operator()( const string &name1, const string &name2 ) const {
        return dates[ name1 ] < dates[ name2 ];
    }
    // dates[ name ] holds year in which Ph.D. degree was granted to name
    static data_map dates;
    // places[ name ] holds instituion that granted Ph.D.
    static data_map places;
};

data_map earlier::dates;
data_map earlier::places;

typedef multiset<string, earlier> date_ordered_mset;
typedef map<string, date_ordered_mset> relation_map;

// Function to output a single branch of the tree, rooted at name
void output_tree( const string& name, relation_map& students, data_map& places,
                  data_map& dates, int indentation_level = 0 ) {
    for( int k = 0 ; k != indentation_level ; ++k ) {
        cout << "       ";
    }

    cout << name << " (" << places[ name ] << " " << dates[ name ] << ")" << endl;

    date_ordered_mset& L = students[ name ];
    date_ordered_mset::const_iterator j;
    for( j = L.begin() ; j != L.end() ; ++j ) {
        output_tree( *j, students, places, dates, indentation_level + 1 );
    }
}

// Function to get a string of all the characters up to next terminator
void get_chunk( istream& in, string& s, char terminator = '\t' ) {
    s.erase( s.begin(), s.end() );
    s.reserve( 20 );
    string::value_type ch;
    while( in.get( ch ) && ch != terminator ) {
        s.insert( s.end(), ch );
    }
}

int main() {
    cout << "Displaying the SIGACT Theoretical Computer Science Genealogy" << endl;
    // Scan the theory database file and build the maps
    cout << "First, enter the name of the file containing the genealogy data: " << flush;
    string file_name;
    cin >> file_name;
    ifstream ifs( file_name.c_str() );
    if( !ifs.is_open() ) {
        cout << "Unable to open " << file_name << endl;
        exit( 1 );
    }

    relation_map advisors, students;
    string name, advisor, place, date;
    while( true ) {
        if( ifs.peek() == '#' ) {
            get_chunk( ifs, name, '\n' );
            continue;
        }
        get_chunk( ifs, name );
        if( !ifs ) break;
        get_chunk( ifs, advisor );
        get_chunk( ifs, place );
        get_chunk( ifs, date, '\n' );

        earlier::places[ name ] = place;
        earlier::dates[ name ] = date;
        if( advisor == "?" ) advisor = "---";
        students[ advisor ].insert( name );
        advisors[ name ].insert( advisor );
    }

    // Find persons with unknown advisor and add a root entry for each
    date_ordered_mset& roots = students[ "---" ];
    relation_map::iterator i;
    date_ordered_mset::iterator j;
    bool any_advisor;
    for( i = advisors.begin() ; i != advisors.end() ; ++i ) {
        any_advisor = false;
        for( j = i->second.begin() ; j != i->second.end() ; ++j ) {
            if( *j == string( "---" ) || advisors.find( *j ) != advisors.end() ) {
                any_advisor = true;
            }
        }

        if( !any_advisor ) {
            string first_advisor = *( i->second.begin() );
            if( find( roots.begin(), roots.end(), first_advisor ) == roots.end() ) {
                roots.insert( first_advisor );
            }
        }
    }

    // Output all the trees rooted at ---
    for( j = roots.begin() ; j != roots.end() ; ++j ) {
        output_tree( *j, students, earlier::places, earlier::dates );
    }

    return 0;
}
