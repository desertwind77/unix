// Demonstrating the STL vector push_back and insert functions
#include <iostream>
#include <cassert>
#include <vector>
#include <string>
#include <algorithm>  // for reverse
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main() 
{
  vector<char> vector1 = 
                   make< vector<char> >("Bjarne Stroustrup"),
               vector2;
  vector<char>::iterator i;

  cout << "Demonstrating vector push_back function" << endl;
  for (i = vector1.begin(); i != vector1.end(); ++i)
    vector2.push_back(*i);
  assert (vector1 == vector2);

  vector1 = make< vector<char> >("Bjarne Stroustrup");
  vector2 = make< vector<char> >("");
   
  cout << "Demonstrating vector insertion at beginning" 
       << endl;
  for (i = vector1.begin(); i != vector1.end(); ++i)
    vector2.insert(vector2.begin(), *i);
  assert (vector2 == 
          make< vector<char> >("purtsuortS enrajB"));

  // Show that vector2 is the reverse of vector1, by using
  // the generic reverse function to reverse vector1:
  reverse(vector1.begin(), vector1.end());
  assert (vector2 == vector1);
  cout << " --- Ok." << endl;
  return 0;
}
