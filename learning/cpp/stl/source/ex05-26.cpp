// Illustrating the generic set operations
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
  cout << "Illustrating the generic set operations." << endl;
  bool result;

  vector<char> vector1 = make< vector<char> >("abcde"),
               vector2 = make< vector<char> >("aeiou");

  // Illustrate includes:
  result = includes(vector1.begin(), vector1.end(),
                    vector2.begin(), vector2.end());
  assert (result == false);

  result = includes(vector1.begin(), vector1.end(),
                    vector2.begin(), vector2.begin() + 2);
  // 'a' and 'e' are contained in vector1
  assert (result == true);

  // Illustrate set_union:
  vector<char> setUnion;
  set_union(vector1.begin(), vector1.end(),
            vector2.begin(), vector2.end(),
            back_inserter(setUnion));

  assert (setUnion == make< vector<char> >("abcdeiou"));

  // Illustrate set_intersection:
  vector<char> setIntersection;
  set_intersection(vector1.begin(), vector1.end(),
        vector2.begin(), vector2.end(),
        back_inserter(setIntersection));

  assert (setIntersection == make< vector<char> >("ae"));

  // Illustrate set_symmetric_difference:
  vector<char> setDifference;

  set_symmetric_difference(vector1.begin(),
        vector1.end(),
        vector2.begin(), vector2.end(),
        back_inserter(setDifference));

  assert (setDifference == make< vector<char> >("bcdiou"));
  cout << " --- Ok." << endl;
  return 0;
}
