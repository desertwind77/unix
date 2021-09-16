// Illustrating the generic swap_ranges algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main()
{
  cout << "Illustrating the generic swap_ranges algorithm." 
       << endl;
  vector<char> vector1 = make< vector<char> >("HELLO"),
               vector2 = make< vector<char> >("THERE");

  // Save vector1 and vector2 contents, for checking:
  vector<char> temp1 = vector1, temp2 = vector2;

  // Swap the contents of vector1 and vector2:
  swap_ranges(vector1.begin(), vector1.end(), 
              vector2.begin());

  assert (vector1 == temp2 && vector2 == temp1);
  cout << " --- Ok." << endl;
  return 0;
}
