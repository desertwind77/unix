#include <iostream>
#include <queue>
using namespace std;

int main() {
    int thedata[] = { 45, 34, 56, 27, 71, 50, 62 };
    priority_queue<int> pq;
    int i;

    for( i = 0 ; i < 4 ; ++i )
        pq.push( thedata[ i ] );
    for( i = 0 ; i < 3 ; ++i ) {
        cout << pq.top() << endl;
        pq.pop();
    }
    cout << endl;
    for( i = 4 ; i < 7 ; ++i )
        pq.push( thedata[ i ] );
    while( !pq.empty() ) {
        cout << pq.top() << endl;
        pq.pop();
    }
    return 0;
}
