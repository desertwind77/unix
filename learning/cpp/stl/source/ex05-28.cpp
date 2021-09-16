// Illustrating the generic min_element and
// max_element algorithms
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic min_element and"
       << " max_element algorithms." << endl;
  // Initialize a vector of integers: 
  vector<int> vector1(5);
  for(int i = 0; i < 5; ++i) 
    vector1[i] = i;
  random_shuffle(vector1.begin(), vector1.end());

  // Find the maximum element in vector1:
  vector<int>::iterator k = 
    max_element(vector1.begin(), vector1.end());
  assert (*k == 4);

  // Find the minimum element in vector1:
  k = min_element(vector1.begin(), vector1.end());
  assert (*k == 0);
  cout << " --- Ok." << endl;
  return 0;
}
