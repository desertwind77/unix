#include <algorithm>
#include <cassert>
#include <deque>
#include <iostream>
#include <iterator>
#include <list>
#include <vector>

using namespace std;


void input1() {
    istream_iterator<char> in( cin );
    // This is any iterator. We don't care because we will stop when we find
    // the first 'x'.
    istream_iterator<char> eos;
    find( in, eos, 'x' );

    cout << "The first non-whitespace character following the first 'x' was '"
         << *(++in) << "'."<< endl;
}

void input2() {
    // Using loop to accept input from standard input
    istream_iterator<string> in( cin );
    istream_iterator<string> eos;

    while( *in != "end" ) {
        cout << "input = " << *in << endl;
        ++in;
    }
}

// This is the STL implementation of copy
// Only InputIterator is needed because copy just do read but no write.
template <typename InputIterator, typename OutputIterator>
OutputIterator myCopy( InputIterator first, InputIterator last,
                    OutputIterator result ) {
    while( first != last ) {
        *result = *first;
        ++first;
        ++result;
    }

    return result;
}

template <typename ForwardIterator, typename T>
void myReplace( ForwardIterator first, ForwardIterator last,
              const T &x, const T &y ) {
    while( first != last ) {
        if( *first == x ) {
            *first = y;
        }
        ++first;
    }
}

int main() {
    int a[ 10 ] = { 12, 3, 25, 7, 11, 213, 7, 123, 29, -31 };
    int *ptr = find( &a[ 0 ], &a[ 10 ], 7 );
    assert( *ptr == 7 && *( ptr + 1 ) == 11 );

    list<int> list1( &a[ 0 ], &a[ 10 ] );
    list<int>::iterator i = find( list1.begin(), list1.end(), 7 );
    assert( *i == 7 && *( ++i ) == 11 );

    int b[ 10 ];
    copy( &a[ 0 ], &a[ 10 ], &b[ 0 ] );
    myReplace( &b[ 0 ], &b[ 10 ], 7, 9 );

    // print output
    ostream_iterator<int> out( cout, " " );
    copy( &b[ 0 ], &b[ 10 ], out );
    cout << endl;

    // reverse require bidirectional iterator which is forward iterator
    // plus both prefix and postfix version of --.
    reverse( &b[ 0 ], &b[ 10 ] );
    copy( &b[ 0 ], &b[ 10 ], out );
    cout << endl;

    // binary_search requires random access iterator.
    //bool found = binary_search( &b[ 0 ], &b[ 10 ], 213 );
    vector<int> v1( &b[ 0 ], &b[ 10 ] );
    bool found = binary_search( v1.begin(), v1.end(), 213 );
    // somehow reverse makes the search result not found
    cout << "search result = " << found << endl;

    vector<int> v2;
    deque<int> deque1( 200, 1 );    // deque1 holds 200 1's.
    // This will cause segmentation fault.
    //copy( deque1.begin(), deque1.end(), v2.begin() );
    copy( deque1.begin(), deque1.end(),
          back_insert_iterator< vector<int> >( v2 ) );
    copy( v2.begin(), v2.end(), out );
    copy( deque1.begin(), deque1.end(), back_inserter( v2 ) );
    cout << endl;
    copy( v2.begin(), v2.end(), out );
    cout << endl;
    list<int> list2;
    copy( v2.begin(), v2.end(), front_inserter( list2 ) );
    deque<int> deque2( v2.begin(), v2.end() );
    copy( v2.begin(), v2.end(), inserter( deque2, deque2.begin() + 1 ) ); 

    merge( v1.begin(), v1.end(), &a[ 0 ], &a[ 10 ],
           ostream_iterator<int>( cout, " " ) );
    cout << endl;

    return 0;
}
