// Illustrating the generic binary search algorithms
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic binary search algorithms." 
       << endl;
  vector<int> v(5);
  bool found;

  // Initialize:
  int i;
  for (i = 0; i < 5; ++i) v[i] = i; 
 
  // Search for each of the integers 0, 1, 2, 3, 4:
  for (i = 0; i < 5; ++i) {
    found = binary_search(v.begin(), v.end(), i);
    assert (found == true);
  }

  // Try searching for a value that's not present:
  found = binary_search (v.begin(), v.end(), 9);
  assert (found == false);

  v[1] = 7; v[2] = 7; v[3] = 7; v[4] = 8;

  // Vector v now contains 0 7 7 7 8

  // Apply upper_bound, lower_bound and equal_range on v:
 
  vector<int>::iterator k;
  k = lower_bound(v.begin(), v.end(), 7);
  assert (k == v.begin() + 1 && *k == 7);

  k = upper_bound(v.begin(), v.end(), 7);
  assert (k == v.end() - 1 && *k == 8);

  pair<vector<int>::iterator, vector<int>::iterator> pi = 
      equal_range(v.begin(), v.end(), 7);

  assert (pi.first == v.begin() + 1);
  assert (pi.second == v.end() - 1);
  cout << " --- Ok." << endl;
  return 0;
}
