#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;

int main() {
    cout << "Enter dictionary name: ";
    string dictionary_name;
    cin >> dictionary_name;
    ifstream ifs( dictionary_name.c_str() );
    if( !ifs.is_open() ) {
        cout << "Unable to open " << dictionary_name << endl;
        exit( 1 );
    }

    typedef istream_iterator<string> string_input;
    vector<string> dictionary;
    copy( string_input( ifs ), string_input(), back_inserter( dictionary ) );
    cout << "Dictionary contains " << dictionary.size() << " word." << endl;

    cout << "Enter a word: ";
    for( string_input j( cin ) ; j != string_input() ; ++j ) {
        string word = *j;
        sort( word.begin(), word.end() );
        bool found_one = false;

        do {
            if( binary_search( dictionary.begin(), dictionary.end(), word ) ) {
                cout << " " << word << endl;
                found_one = true;
            }
        } while( next_permutation( word.begin(), word.end() ) );

        cout << "Enter a word: ";
    }

    return 0;
}
