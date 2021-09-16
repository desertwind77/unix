#include <vector>
#include <iostream>
using namespace std;

int main() {
    const long N = 600000;
    const long S = 10;

    vector<double> x(N), y(N);
    long k;

    for( k = 0 ; 3 * k * S < N ; ++k )
        x[ 3 * k * S ] = 1.0;
    for( k = 0 ; 5 * k * S < N ; ++k )
        y[ 5 * k * S ] = 1.0;

    double sum = 0.0;
    for( k = 0 ; k < N ; ++k )
        sum += x[ k ] * y[ k ];

    return 0;
}
