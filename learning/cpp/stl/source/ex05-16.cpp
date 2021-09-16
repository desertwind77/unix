// Illustrating the generic replace algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;

int main()
{
  cout << "Illustrating the generic replace algorithm." 
       << endl;
  string s("FERRARI");
  vector<char> vector1(s.begin(), s.end());

  // Replace all occurrences of R by S:
  replace(vector1.begin(), vector1.end(), 'R', 'S');

  assert (string(vector1.begin(), vector1.end()) ==
         string("FESSASI"));
  cout << " --- Ok." << endl;
  return 0;
}
