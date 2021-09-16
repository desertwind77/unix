#include <algorithm>
#include <cassert>
#include <functional>
using namespace std;

int main() {
    int a[] = { 0, 0, 0, 1, 1, 1, 2, 2, 2 };
    int final_count = count( &a[ 0 ], &a[ 9 ], 1 );
    assert( final_count == 3 );

    final_count = count_if( &a[ 0 ], &a[ 9 ],
            bind2nd( not_equal_to<int>(), 1 ) );
    assert( final_count == 6 );

    return 0;
}
