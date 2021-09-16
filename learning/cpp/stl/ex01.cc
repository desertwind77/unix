#include <list>
#include <vector>
#include <string.h>

using namespace std;

template < typename T1, typename T2 >
class MyPair {
    public:
        T1 first;
        T2 second;
        MyPair() : first( T1() ), second( T2() ) {}
        MyPair( const T1 &x, const T2 &y ) : first( x ), second( y ) {}
};

bool operator<( const MyPair< double, long > &x,
                const MyPair< double, long > &y ) {
    return x.first < y.first;
}

template < typename T >
const T& max( T &x, T &y ) {
    if( x < y ) {
        return y;
    } else {
        return x;
    }
}

vector<char> vec( const char s[] ) {
    return vector<char>( &s[ 0 ], &s[ strlen( s ) ] );
}

list<char> lst( const char s[] ) {
    return list<char>( &s[ 0 ], &s[ strlen( s ) ] );
}

template < typename Container >
Container make( const char s[] ) {
    return Container( &s[ 0 ], &s[ strlen( s ) ] );
}

int main() {
    MyPair< double, long > a( 1.1, 2 );
    MyPair< double, long > b( 2.1, 3 );
    MyPair< double, long > c = max( a, b );

    char myString[] = "This is my string.";
    vector<char> v = vec( myString );
    list<char> l = lst( myString );
    list<char> l2 = make< list< char > >( myString  );

    return 0;
}
