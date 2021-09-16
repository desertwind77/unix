#include <iostream>
#include <list>
#include <queue>
using namespace std;

int main() {
    int thedata[] = { 45, 34, 56, 27, 71, 50, 62 };
    queue<int, list<int> > q;
    int i;

    for( i = 0 ; i < 4 ; ++i )
        q.push( thedata[ i ] );
    for( i = 0 ; i < 3 ; ++i ) {
        cout << q.front() << endl;
        q.pop();
    }
    for( i = 4 ; i < 7 ; ++i )
        q.push( thedata[ i ] );
    while( !q.empty() ) {
        cout << q.front() << endl;
        q.pop();
    }
    return 0;
}
