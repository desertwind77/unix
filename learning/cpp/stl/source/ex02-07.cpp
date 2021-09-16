// Demonstrating the generic find algorithm with a list
#include <iostream>
#include <cassert>
#include <list>
#include <algorithm> // for find
using namespace std; 
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}
  
int main()
{
  cout << "Demonstrating generic find algorithm with "
       << "a list." << endl;
 
  list<char> list1 = make< list<char> >("C++ is a better C");

  // Search for the first occurrence of the letter e:
  list<char>::iterator
    where = find(list1.begin(), list1.end(), 'e');

  list<char>::iterator next = where;
  ++next;
  assert (*where == 'e' && *next == 't');
  cout << " --- Ok." << endl;
  return 0;
}
