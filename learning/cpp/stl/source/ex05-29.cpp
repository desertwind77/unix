// Illustrating the generic lexicographical_compare algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main()
{
  cout << "Illustrating the generic" 
       << " lexicographical_compare algorithm." << endl;

  vector<char> vector1 = make< vector<char> >("helio");
  vector<char> vector2 = make< vector<char> >("hello");

  // Show that vector1 is lexicographically 
  // less than vector2:
  bool result = lexicographical_compare(vector1.begin(),
          vector1.end(), vector2.begin(), vector2.end());

  assert (result == true);
  cout << " --- Ok." << endl;
  return 0;
}
