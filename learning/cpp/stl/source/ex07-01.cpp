// Demonstrating set construction and insertion
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
  cout << "Demonstrating set construction and insertion."
       << endl;
  list<char> list1 = 
      make< list<char> >("There is no distinctly native "
                         "American criminal class");
  
  // Put the characters in list1 into set1:
  set<char> set1;
  list<char>::iterator i;
  for (i = list1.begin(); i != list1.end(); ++i)
    set1.insert(*i);
  
// Put the characters in set1 into list2:
  list<char> list2;
  set<char>::iterator k;
  for (k = set1.begin(); k != set1.end(); ++k)
    list2.push_back(*k);

  assert (list2 == make< list<char> >(" ATacdehilmnorstvy"));
  return 0;
}
