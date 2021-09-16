// Using reverse_copy, a copying version of the 
// generic reverse algorithm
#include <iostream>
#include <algorithm>
#include <cassert>
using namespace std;

int main() {
  cout << "Using reverse_copy, a copying version of the"
       << " generic reverse algorithm." << endl;
  int a[1000], b[1000];
  int i;
  for (i = 0; i < 1000; ++i) 
    a[i] = i;

  reverse_copy(&a[0], &a[1000], &b[0]);
 
  for (i = 0; i < 1000; ++i) 
     assert (a[i] == i && b[i] == 1000 - i - 1);
  cout << " --- Ok." << endl;
  return 0;
}
