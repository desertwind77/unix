#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

class GreaterThan50 {
    public:
        bool operator()( int &x ) const {
            return x > 50;
        }
};

int main() {
    vector<int> vector1;

    for( int i = 0 ; i < 13 ; ++i ) {
        vector1.push_back( i * i );
    }

    vector<int>::iterator where = find_if( vector1.begin(), vector1.end(),
                                           GreaterThan50() );
    assert( *where == 64 );

    return 0;
}
