// Illustrating the generic permutation algorithms
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic permutation algorithms." 
       << endl;
  // Initialize a vector of integers: 
  vector<int> vector1(3);
  for (int i = 0; i < 3; ++i) vector1[i] = i;

  // In lexicographical order the permutations of 0 1 2 are
  // 0 1 2, 0 2 1, 1 0 2, 1 2 0, 2 0 1, 2 1 0. 
  // Show that from 0 1 2 next_permutation produces 0 2 1:
  next_permutation(vector1.begin(), vector1.end());
  assert (vector1[0] == 0);
  assert (vector1[1] == 2);
  assert (vector1[2] == 1);

  // Show that from 0 2 1 prev_permutation() produces 0 1 2:
  prev_permutation(vector1.begin(), vector1.end());
  assert (vector1[0] == 0);
  assert (vector1[1] == 1);
  assert (vector1[2] == 2);
  cout << " --- Ok." << endl;
  return 0;
}
