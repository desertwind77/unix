#include <iostream>
#include <stack>
using namespace std;

int main() {
    int thedata[] = { 45, 34, 56, 27, 71, 50, 62 };
    stack<int> s;
    int i;

    for( i = 0 ; i < 4 ; ++i )
        s.push( thedata[ i ] );
    for( i = 0 ; i < 3 ; ++i ) {
        cout << s.top() << endl;
        s.pop();
    }
    for( i = 4 ; i < 7 ; ++i )
        s.push( thedata[ i ] );
    while( !s.empty() ) {
        cout << s.top() << endl;
        s.pop();
    }
    return 0;
}
