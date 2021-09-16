// Demonstrating the STL list sort and unique functions
#include <iostream>
#include <cassert>
#include <string>
#include <list>
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main() 
{
  cout << "Demonstrating STL list sort and unique "
       << "functions." << endl;
  list<char> list1 = make< list<char> >("Stroustrup");

  list1.sort();
  assert (list1 == make< list<char> >("Soprrsttuu"));

  list1.unique();
  assert (list1 == make< list<char> >("Soprstu"));
  cout << " --- Ok." << endl;
  return 0;
}
