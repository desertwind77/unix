// Illustrating the generic merge algorithms
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic merge algorithms." << endl;
  // Initialize vector of integers: 
  vector<int> vector1(5);
  vector<int> vector2(5);
  vector<int> vector3(10);

  int i;
  for (i = 0; i < 5; ++i) 
    vector1[i] = 2 * i;
  
  for (i = 0; i < 5; ++i)
    vector2[i] = 1 + 2 * i;

  // Merge contents of vector1 and vector2,
  // putting result in vector3:
  merge(vector1.begin(), vector1.end(),
        vector2.begin(), vector2.end(),
        vector3.begin());
  
  for (i = 0; i < 10; ++i)
    assert (vector3[i] == i);

  for (i = 0; i < 5; ++i)
    vector3[i] = vector1[i];
  for (i = 0; i < 5; ++i)
    vector3[i + 5] = vector2[i];

  // Merge the two sorted halves of vector3
  // in place to obtain a sorted vector3:
  inplace_merge(vector3.begin(), vector3.begin() + 5,
                vector3.end());

  for (i = 0; i < 10; ++i)
    assert (vector3[i] == i);
  cout << " --- Ok." << endl;
  return 0;
}
