#include <algorithm>
#include <cassert>
#include <functional>
#include <iostream>
#include <iomanip>
#include <vector>
using namespace std;

template <typename T>
class less_with_count : public binary_function<T, T, bool> {
 public:
    less_with_count() : counter( 0 ), progenitor( 0 ) {}
    // copy constructor
    less_with_count( less_with_count<T>& x ) : counter( 0 ),
        progenitor( x.progenitor ? x.progenitor : &x ) {}
    bool operator()( const T& x, const T& y ) {
        ++counter;
        return x < y;
    }
    long report() const { return counter; }
    ~less_with_count() {    // Destructor
        if( progenitor ) {
            progenitor->counter += counter;
        }
    }
 private:
    long counter;
    less_with_count<T> *progenitor;
};

int main() {
    const long N1 = 1000, N2 = 128000;

    for( long N = N1 ; N <= N2 ; N *= 2 ) {
        vector<int> v1;
        for( int k = 0 ; k < N ; ++k )
            v1.push_back( k );
        random_shuffle( v1.begin(), v1.end() );
        less_with_count<int> comp_counter;
        sort( v1.begin(), v1.end(), comp_counter );
        cout << "Problem size " << setw( 9 ) << N
             << ", comparisons performed: " << setw( 9 )
             << comp_counter.report() << endl;
    }

    return 0;
}
