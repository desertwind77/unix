#include <algorithm>
#include <cassert>
#include <iostream>
#include <iterator>
#include <vector>
using namespace std;

int main() {
    vector<int> v1( 5 );
    int i;

    for( i = 0 ; i < 5 ; ++i ) {
        v1[ i ] = i;
    }

    ostream_iterator<int> out( cout, " " );

    // top of the heap is max
    
    random_shuffle( v1.begin(), v1.end() );
    cout << "random:    ";
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    // sort v1 using push_heap and pop_heap
    for( i = 2 ; i < 5 ; ++i ) {
        push_heap( v1.begin(), v1.begin() + i );
    }
    cout << "push_heap: ";
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    for( i = 5 ; i >= 2 ; --i ) {
        pop_heap( v1.begin(), v1.begin() + i );
    }
    cout << "pop_heap:  ";
    copy( v1.begin(), v1.end(), out );
    cout << endl << endl;

    for( i = 0 ; i < 5 ; ++i ) {
        assert( v1[ i ] == i );
    }

    random_shuffle( v1.begin(), v1.end() );
    cout << "random:    ";
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    // sort v1 using make_heap and sort_heap
    make_heap( v1.begin(), v1.end() );
    cout << "make_heap: ";
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    sort_heap( v1.begin(), v1.end() );
    cout << "sort_heap: ";
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    for( i = 0 ; i < 5 ; ++i ) {
        assert( v1[ i ] == i );
    }

    return 0;
}
