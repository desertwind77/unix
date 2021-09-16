// Illustrating the generic fill and fill_n algorithms
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;

int main()
{
  cout << "Illustrating the generic fill "
       << "and fill_n algorithms." << endl;
  string s("Hello there");
  vector<char> vector1(s.begin(), s.end());

  // Fill first 5 positions of vector1 with X's:
  fill(vector1.begin(), vector1.begin() + 5, 'X');

  assert (string(vector1.begin(), vector1.end()) == 
         string("XXXXX there"));

  // Fill 3 more positions with Y's:
  fill_n(vector1.begin() + 5, 3, 'Y');

  assert (string(vector1.begin(), vector1.end()) ==
         string("XXXXXYYYere"));
  cout << " --- Ok." << endl;
  return 0;
}
