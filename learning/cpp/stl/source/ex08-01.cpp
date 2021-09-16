// Demonstrating function pointer passing.
#include <iostream>
#include <cassert>
#include <vector>
using namespace std;

template <typename InputIterator, typename T>
T accumulate1(InputIterator first, InputIterator last, T init, 
             T (*binary_function)(T x, T y)) // New parameter
{
  while (first != last) {
    init = (*binary_function)(init, *first);
    ++first;
  }
  return init;
}
 
int multfun(int x, int y) { return x * y; }

int main()
{
  cout << "Demonstrating function pointer passing." << endl;
  int x[5] = {2, 3, 5, 7, 11};
  // Initialize vector1 to x[0] through x[4]:
  vector<int> vector1(&x[0], &x[5]); 
  
  int product = accumulate1(vector1.begin(), vector1.end(), 
                            1, &multfun);
  assert (product == 2310);
  cout << " --- Ok." << endl;
  return 0;
}
