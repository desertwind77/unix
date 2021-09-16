// Illustrating the generic heap operations
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic heap operations." << endl;
  // Initialize a vector of integers: 
  vector<int> vector1(5);
  int i;
  for (i = 0; i < 5; ++i)
    vector1[i] = i;

  random_shuffle(vector1.begin(), vector1.end());

  // Sort vector1 using push_heap and pop_heap:
  for (i = 2; i <= 5; ++i)
    push_heap(vector1.begin(), vector1.begin() + i);
  
  for (i = 5; i >= 2; --i)
    pop_heap(vector1.begin(), vector1.begin() + i);
  
  // Verify that the array is sorted:
  for (i = 0; i < 5; ++i)   
    assert (vector1[i] == i);

  // Shuffle the elements again:
  random_shuffle(vector1.begin(), vector1.end());

  // Sort vector1 using make_heap and sort_heap:
  make_heap(vector1.begin(), vector1.end());
  sort_heap(vector1.begin(), vector1.end());

  // Verify that the array is sorted:
  for (i = 0; i < 5; ++i) 
     assert (vector1[i] == i);
  cout << " --- Ok." << endl;
  return 0;
}
