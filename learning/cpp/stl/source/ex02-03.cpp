// Demonstrating generic reverse algorithm on a list
#include <iostream>
#include <cassert>
#include <list>
#include <algorithm>  // For reverse
using namespace std; 
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main()
{
  cout << "Demonstrating generic reverse algorithm on a list" 
      << endl;
  list<char> list1 = make< list<char> >("mark twain");
  reverse(list1.begin(), list1.end());
  assert (list1 == make< list<char> >("niawt kram"));
  cout << " --- Ok." << endl;
  return 0;
}
