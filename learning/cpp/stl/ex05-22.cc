#include <algorithm>
#include <iterator>
#include <iostream>
#include <vector>
using namespace std;

class comp_last {
 public:
    bool operator()( int x, int y ) {
        return ( x % 10 ) <  ( y % 10 );
    }
};

int main() {
    const int N = 20;

    vector<int> v0;
    for( int i = 0 ; i < N ; ++i ) {
        v0.push_back( i );
    }

    vector<int> v1 = v0;
    ostream_iterator<int> out( cout, " " );

    cout << "Before sorting:" << endl;
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    sort( v1.begin(), v1.end(), comp_last() );

    cout << "After sorting:" << endl;
    copy( v1.begin(), v1.end(), out );
    cout << endl;
    
    v1 = v0;
    stable_sort( v1.begin(), v1.end(), comp_last() );
    cout << "After stable_sorting:" << endl;
    copy( v1.begin(), v1.end(), out );
    cout << endl;

    v1 = v0;
    partial_sort( v1.begin(), v1.begin() + 5, v1.end(), comp_last() );
    cout << "After partial_sorting:" << endl;
    copy( v1.begin(), v1.end(), out );
    cout << endl;

}
