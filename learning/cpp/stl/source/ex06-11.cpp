// Demonstrating the STL list erase function
#include <iostream>
#include <cassert>
#include <list>
#include <string>
#include <algorithm>  // for find
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main() 
{
  cout << "Demonstrating STL list erase function." << endl;
  list<char> list1 = make< list<char> >("remembering");
  list<char>::iterator j;

  j = find(list1.begin(), list1.end(), 'i');

  list1.erase(j++); 
  assert (list1 == make< list<char> >("rememberng"));
  
  // j now points to the 'n':
  list1.erase(j++); 
  assert (list1 == make< list<char> >("rememberg"));

  // j now points to the 'g':
  list1.erase(j++); 
  assert (list1 == make< list<char> >("remember"));
  list1.erase(list1.begin()); 
  assert (list1 == make< list<char> >("emember"));

  list1.erase(list1.begin());
  assert (list1 == make< list<char> >("member"));
  cout << " --- Ok." << endl;
  return 0;
}
