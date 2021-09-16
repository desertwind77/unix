// Illustrating the generic accumulate algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <functional>
#include <numeric>
using namespace std;

int main()
{
  cout << "Illustrating the generic accumulate algorithm." 
       << endl;
  int x[20];
  
  for (int i = 0; i < 20; ++i)
    x[i] = i;

  // Show that 5 + 0 + 1 + 2 + ... + 19 == 195:
  int result = accumulate(&x[0], &x[20], 5);
  assert (result == 195);

  // Show that 10 * 1 * 2 * 3 * 4 == 240:
  result = accumulate(&x[1], &x[5], 10, multiplies<int>());
  assert (result == 240);
  cout << " --- Ok." << endl;
  return 0;
}
