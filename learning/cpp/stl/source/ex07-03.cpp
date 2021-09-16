// Demonstrating multiset erase functions
#include <iostream>
#include <cassert>
#include <list>
#include <string>
#include <set>
using namespace std; 
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}
#include <functional>
template <typename Container>
string make_string(const Container& c)
{
  string s;
  copy(c.begin(), c.end(), inserter(s, s.end()));
  return s;
}

int main()
{
  cout << "Demonstrating multiset erase functions" << endl;
  list<char> list1 = 
      make< list<char> >("There is no distinctly native "
                         "American criminal class");

  // Put the characters in list1 into multiset1:
  multiset<char> multiset1;
  copy(list1.begin(), list1.end(),
       inserter(multiset1, multiset1.end()));
  assert (make_string(multiset1) ==
      "       ATaaaaccccdeeeehiiiiiiilllmmnnnnnorrrsssstttvy");
  multiset1.erase('a');
  assert (make_string(multiset1) ==
          "       ATccccdeeeehiiiiiiilllmmnnnnnorrrsssstttvy");

  multiset<char>::iterator i = multiset1.find('e');
  
  multiset1.erase(i);
  assert (make_string(multiset1) ==
          "       ATccccdeeehiiiiiiilllmmnnnnnorrrsssstttvy");
  cout << " --- Ok." << endl;
  return 0;
}
