#include <algorithm>
#include <list>
#include <iostream>
#include <string>
using namespace std;

void print_list( string s ) {
    cout << s << endl;
}

int main() {
    list<string> dlist;
    dlist.insert( dlist.end(), "Clark" );
    dlist.insert( dlist.end(), "Rindt" );
    dlist.insert( dlist.end(), "Senna" );
    
    for_each( dlist.begin(), dlist.end(), print_list );

    return 0;
}
