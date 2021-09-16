// Using the generic accumulate algorithm to compute a product,
// using multiplies
#include <iostream>
#include <vector>
#include <cassert>
#include <numeric>  // For accumulate
#include <functional>  // For multiplies
using namespace std; 

int main()
{
  cout << "Using generic accumulate algorithm to "
       << "compute a product." << endl;

  int x[5] = {2, 3, 5, 7, 11};

  // Initialize vector1 to x[0] through x[4]:
  vector<int> vector1(&x[0], &x[5]); 
  
  int product = accumulate(vector1.begin(), vector1.end(),
                           1, multiplies<int>());
    
  assert (product == 2310);
  cout << " --- Ok." << endl;
  return 0;
}
