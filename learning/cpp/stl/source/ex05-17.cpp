// Illustrating the generic rotate algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;

int main()
{
  cout << "Illustrating the generic rotate algorithm." << endl;
  string s("Software Engineering ");
  vector<char> vector1(s.begin(), s.end());

  // Rotate the vector so that "Engineering " comes first:
  rotate(vector1.begin(), vector1.begin() + 9,
         vector1.end());

  assert (string(vector1.begin(), vector1.end()) == 
          string("Engineering Software "));
  cout << " --- Ok." << endl;
  return 0;
}
