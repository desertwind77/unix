#include <cassert>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    char name[] = "George Foreman";
    vector<char> George( name, name + 6 );

    vector<char> anotherGeorge( George.begin(), George.end() );
    assert( George == anotherGeorge );

    vector<char> son1( George );    // copy constructor
    assert( George == son1 );

    vector<char> son2 = George;    // copy constructor
    assert( George == son2 );

    return 0;
}
