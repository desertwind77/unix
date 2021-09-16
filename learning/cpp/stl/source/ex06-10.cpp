// Demonstrating the STL list push_back and push_front functions
#include <iostream>
#include <cassert>
#include <list>
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
  list<char> list1 = make< list<char> >("Bjarne Stroustrup"), 
             list2;
  list<char>::iterator i;

  cout << "Demonstrating list push_back function" << endl;
  for (i = list1.begin(); i != list1.end(); ++i)
    list2.push_back(*i);
  assert (list1 == list2);

  list1 = make< list<char> >("Bjarne Stroustrup");
  list2 = make< list<char> >("");
   
  cout << "Demonstrating list push_front function" << endl;
  for (i = list1.begin(); i != list1.end(); ++i)
    list2.push_front(*i);
  assert (list2 == make< list<char> >("purtsuortS enrajB"));

  // Show that list2 is the reverse of list1, by using
  // STL generic reverse function to reverse list1:
  reverse(list1.begin(), list1.end());
  assert (list2 == list1);
  cout << " --- Ok." << endl;
  return 0;
}
