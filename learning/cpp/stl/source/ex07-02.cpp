// Demonstrating multiset construction and insertion
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

int main()
{
  cout << "Demonstrating multiset construction "
       << "and insertion." << endl;
  list<char> list1 = 
      make< list<char> >("There is no distinctly native "
                         "American criminal class");
  
  // Put the characters in list1 into multiset1:
  multiset<char> multiset1;
  list<char>::iterator i;
  for (i = list1.begin(); i != list1.end(); ++i)
    multiset1.insert(*i);
  
  // Put the characters in multiset1 into list2:
  list<char> list2;
  multiset<char>::iterator k;
  for (k = multiset1.begin(); k != multiset1.end(); ++k)
    list2.push_back(*k);

  assert (list2 == 
          make< list<char> >("       ATaaaaccccdeeeehiiiiiii"
                             "lllmmnnnnnorrrsssstttvy"));
  cout << " --- Ok." << endl;
  return 0;
}
