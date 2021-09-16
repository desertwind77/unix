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
    less_with_count() {}
    bool operator()( const T& x, const T& y ) {
        ++counter;
        return x < y;
    }
    long report() const { return counter; }
    static long counter;
};

template <typename T>
long less_with_count<T>::counter = 0;

int main() {
    const long N1 = 1000, N2 = 128000;

    for( long N = N1 ; N <= N2 ; N *= 2 ) {
        vector<int> v1;
        for( int k = 0 ; k < N ; ++k )
            v1.push_back( k );
        random_shuffle( v1.begin(), v1.end() );
        less_with_count<int> comp_counter;
        less_with_count<int>::counter = 0;
        sort( v1.begin(), v1.end(), comp_counter );
        cout << "Problem size " << setw( 9 ) << N
             << ", comparisons performed: " << setw( 9 )
             << comp_counter.report() << endl;
    }

    return 0;
}
