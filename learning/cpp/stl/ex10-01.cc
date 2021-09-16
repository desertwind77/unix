#include <iostream>
#include <vector>
#include <list>
using namespace std;

template <typename Container>
void display( const Container &c ) {
    typename Container::const_iterator i;
    for( i = c.begin() ; i != c.end() ; ++i )
        cout << *i << " ";
    cout << endl;

    typename Container::const_reverse_iterator r;
    for( r = c.rbegin() ; r != c.rend() ; ++r )
        cout << *r << " ";
    cout << endl;
}

int main() {
    vector<int> v1;
    v1.push_back( 2 );
    v1.push_back( 3 );
    v1.push_back( 5 );
    v1.push_back( 7 );
    v1.push_back( 11 );

    display( v1 );

    list<int> l1( v1.begin(), v1.end() );
    display( l1 );

    return 0;
}
