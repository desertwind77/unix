// Demonstrating multiset search member functions
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
  cout << "Demonstrating multiset search member functions." 
       << endl;
  list<char> list1 = 
      make< list<char> >("There is no distinctly native "
                         "American criminal class"),
             list2 = 
      make< list<char> >("except Congress. - Mark Twain");

  // Put the characters in list1 into multiset1:
  multiset<char> multiset1;
  copy(list1.begin(), list1.end(),
       inserter(multiset1, multiset1.end()));

  assert (make_string(multiset1) == 
      "       ATaaaaccccdeeeehiiiiiiilllmmnnnnnorrrsssstttvy");

  multiset<char>::iterator i = multiset1.lower_bound('c'),
                           j = multiset1.upper_bound('r');
  
  multiset1.erase(i, j);

  assert (make_string(multiset1) == "       ATaaaasssstttvy");
  
  list<char> found, not_found;
  list<char>::iterator k;
  for (k = list2.begin(); k != list2.end(); ++k)
    if (multiset1.find(*k) != multiset1.end())
      found.push_back(*k);
    else
      not_found.push_back(*k);

  assert (found == make< list<char> >("t ss  a Ta"));
  assert (not_found == 
          make< list<char> >("excepCongre.-Mrkwin"));
  cout << " --- Ok." << endl;
  return 0;
}
