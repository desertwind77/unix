// Illustrating the generic nth_element algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic nth_element algorithm." 
       << endl;
  vector<int> v(7);

  v[0] = 25; v[1] = 7; v[2] = 9;
  v[3] = 2; v[4] = 0; v[5] = 5; v[6] = 21;

  const int N = 4;

  // Use nth_element to place the Nth smallest 
  // element in v in the Nth position, v.begin() + N:

  nth_element(v.begin(), v.begin() + N, v.end());
  
  // Check that the element at v.begin() + N, v[N], is
  // greater than or equal to each of the preceding elements:
  int i;
  for (i = 0; i < N; ++i)
    assert (v[N] >= v[i]);
  
  // Check that v[N] is less than or equal to each 
  // of the following elements:
  for (i = N + 1; i < 7; ++i)
    assert (v[N] <= v[i]);
  cout << " --- Ok." << endl;
  return 0;
}
