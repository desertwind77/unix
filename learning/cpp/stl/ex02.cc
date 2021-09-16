#include <algorithm>
#include <cassert>
#include <cstring>
#include <deque>
#include <iostream>
#include <list>
#include <map>
#include <numeric>  // for accumulate
#include <string>
#include <vector>

using namespace std;

template <typename Container>
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

template <typename InputIterator, typename T>
T myAccumulate( InputIterator first, InputIterator last, T init ) {
    while( first != last ) {
        init = init + *first;
        ++first;
    }

    return init;
}

int mult( int x, int y ) { return x * y; }

class multiply {
    public:
        int operator()( int x, int y ) const { return x * y; }
};

template <typename T>
class myMult {
    public:
        int operator()( const T &x, const T &y ) const {
            return x * y;
        }
};

int main() {
    // To demonstrate reverse algorithm
    string string1 = "mark twain";
    reverse( string1.begin(), string1.end() );
    assert( string1 == "niawt kram" );

    char array1[] = "mark twain";
    int N1 = strlen( array1 );
    reverse( &array1[ 0 ], &array1[ N1 ] );
    assert( string( array1 ) == "niawt kram" );

    vector<char> v1 = make< vector<char> >( "mark twain" );
    reverse( v1.begin(), v1.end() );
    assert( v1 == make< vector<char> >( "niawt kram" ) );

    list<char> l1 = make< list<char> >( "mark twain" );
    reverse( l1.begin(), l1.end() );
    assert( l1 == make< list<char> >( "niawt kram" ) );

    // To demonstrate find algorithm
    char s[] = "C++ is a better C";
    int len = strlen( s );
    const char *where1 = find( &s[ 0 ], &s[ len ], 'e' );
    assert( *where1 == 'e' && *( where1 + 1 ) == 't' );

    vector<char> v2 = make< vector<char> >( s );
    vector<char>::iterator where2 = find( v2.begin(), v2.end(), 'e' ); 
    assert( *where2 == 'e' && *( where2 + 1 ) == 't' );

    list<char> l2 = make< list<char> >( s );
    list<char>::iterator where3 = find( l2.begin(), l2.end(), 'e' ); 
    list<char>::iterator next = where3; 
    // *(where3 + 1 ) doesn't work with list because list doesn't support
    // random access iterator.
    ++next;
    assert( *where3 == 'e' && *next  == 't' );

    deque<char> q1 = make< deque<char> >( s );
    deque<char>::iterator where4 = find( q1.begin(), q1.end(), 'e' ); 
    assert( *where4 == 'e' && *( where4 + 1 ) == 't' );

    // To demonstrate merge algorithm
    char s2[] = "acegikm";
    deque<char> q2 = make< deque<char> >( "bdfhjlnopqrstuvwxyz" );
    list<char> l3( 26, 'x' );
    merge( &s2[ 0 ], &s2[ 5 ], q2.begin(), q2.begin() + 10, l3.begin() );
    assert( l3 == make< list<char> >( "abcdefghijlnopqxxxxxxxxxxx" ) );

    // To demonstrate accumulate algorithm
    int x[ 5 ] = { 2, 3, 5, 7, 11 };
    int sum1 = accumulate( &x[ 0 ], &x[ 5 ], 0 );
    assert( sum1 == 28 );
    vector<int> v3( &x[ 0 ], &x[ 5 ] );
    int sum2 = accumulate( v3.begin(), v3.end(), 0 );
    assert( sum2 == 28 );
    list<int> l4( &x[ 0 ], &x[ 5 ] );
    int sum3 = accumulate( l4.begin(), l4.end(), 0 );
    assert( sum3 == 28 );
    int sum4 = myAccumulate< list<int>::iterator, int >( l4.begin(), l4.end(), 0 );
    // Following also works.
    //int sum4 = myAccumulate( l4.begin(), l4.end(), 0 );
    assert( sum4 == 28 );

    // Using function pointer
    int product1 = accumulate( v3.begin(), v3.end(), 1, mult );
    assert( product1 == 2310 );
    // Using function object
    int product2 = accumulate( v3.begin(), v3.end(), 1, multiply() );
    assert( product2 == 2310 );
    // Using STL
    int product3 = accumulate( v3.begin(), v3.end(), 1, multiplies<int>() );
    assert( product3 == 2310 );
    // Using my STL variant
    int product4 = accumulate( v3.begin(), v3.end(), 1, myMult<int>() );
    assert( product4 == 2310 );

	/*
    map<string, long> directory;
    directory[ "Bogart" ] = 1234567;
    directory[ "Bacall" ] = 9876543;
    directory[ "Cagney" ] = 3459873;

    cout << "Please enter name: ";
    string name;
    while( cin >> name ) {
        if( directory.find( name ) != directory.end() ) {
            cout << "The phone number for " << name << " is "
                 << directory[ name ] << endl;
        } else {
            cout << "No listing for " << name << endl;
        }
        cout << "Please enter name:";
    }
    cout << endl;
	*/

    return 0;
}
