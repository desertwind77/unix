// Using an in-place generic sort algorithm
#include <iostream>
#include <algorithm>
#include <cassert>
using namespace std;

int main() {
  cout << "Using an in-place generic sort algorithm." << endl;
  int a[1000];
  int i;
  for (i = 0; i < 1000; ++i) 
    a[i] = 1000 - i - 1;

  sort(&a[0], &a[1000]);

  for (i = 0; i < 1000; ++i) 
    assert (a[i] == i);
  cout << " --- Ok." << endl;
  return 0;
}
