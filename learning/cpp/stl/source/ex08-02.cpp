// Demonstrating function pointer passing.
#include <iostream>
#include <cassert>
#include <vector>
using namespace std;

template <typename InputIterator, typename T, 
          typename BinaryFunction>
T accumulate(InputIterator first, InputIterator last, T init, 
             BinaryFunction binary_function)
{
  while (first != last) {
    init = binary_function(init, *first);
    ++first;
  }
  return init;
}
 
class multiply {
 public:
  int operator()(int x, int y) const { return x * y; }
};

multiply multfunobj;

int main()
{
  cout << "Demonstrating function pointer passing." << endl;
  int x[5] = {2, 3, 5, 7, 11};
  // Initialize vector1 to x[0] through x[4]:
  vector<int> vector1(&x[0], &x[5]); 
  
  int product = accumulate(vector1.begin(), vector1.end(), 
                           1, multfunobj);
  assert (product == 2310);
  cout << " --- Ok." << endl;
  return 0;
}
