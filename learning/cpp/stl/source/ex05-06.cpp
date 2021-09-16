// Illustrating the generic count algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <functional>
using namespace std;

int main()
{
  cout << "Illustrating the generic count algorithm." << endl;
  int a[] = {0, 0, 0, 1, 1, 1, 2, 2, 2};

  // Count the number of values in the array a
  // that are equal to 1:
  int final_count = count(&a[0], &a[9], 1);

  assert (final_count == 3);
  
  // Determine the number of array elements that are not 
  // equal to 1:
  final_count = count_if(&a[0], &a[9], 
                         bind2nd(not_equal_to<int>(), 1));

  // There are 6 elements not equal to 1.
  assert (final_count == 6);
  cout << " --- Ok." << endl;
  return 0;
}
