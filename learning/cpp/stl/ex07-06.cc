#include <map>
#include <iostream>
using namespace std;

int main() {
    const long N = 600000;
    const long S = 10;

    map<long, double> x, y;
    long k;

    for( k = 0 ; 3 * k * S < N ; ++k )
        x[ 3 * k * S ] = 1.0;
    for( k = 0 ; 5 * k * S < N ; ++k )
        y[ 5 * k * S ] = 1.0;

    double sum = 0.0;
    map<long, double>::iterator ix, iy;
    for( sum = 0.0, ix = x.begin() ; ix != x.end() ; ++ix ) {
        long i = ix->first;
        iy = y.find( i );
        if( iy != y.end() )
            sum += ix->second * iy->second;
    }

    return 0;
}
