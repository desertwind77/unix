// Demonstrating the STL list splice functions
#include <iostream>
#include <cassert>
#include <list>
#include <string>
#include <algorithm> // for find
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main() 
{
  cout << "Demonstrating STL splice functions." << endl;
  list<char> list1, list2, list3;
  list<char>::iterator i, j, k;
  
  // Example of splice(iterator, list<char>&):
  list1 = make< list<char> >("There is something "
                             "about science.");
  list2 = make< list<char> >("fascinating ");
  i = find(list1.begin(), list1.end(), 'a');
  list1.splice(i, list2);
  assert (list1 == 
      make< list<char> >("There is something fascinating "
                         "about science."));
  assert (list2 == make< list<char> >(""));

  // Example of splice(iterator, list<char>&, iterator):
  list1 = 
        make< list<char> >("One gets such wholesale return "
                           "of conjecture");
  list2 = 
        make< list<char> >("out of ssuch a trifling "
                           "investment of fact.");
  list3 = make< list<char> >(" of");
  i = search(list1.begin(), list1.end(), list3.begin(),
             list3.end());
  // i points to the blank before "of";
  j = find(list2.begin(), list2.end(), 's');
  list1.splice(i, list2, j);
  assert (list1 == 
      make< list<char> >("One gets such wholesale returns "
                         "of conjecture"));
  assert (list2 == 
      make< list<char> >("out of such a trifling investment "
                         "of fact."));

  // Example of splice(iterator, list<char>&, iterator,
  //                   iterator):
  list1 = make< list<char> >("Mark Twain");
  list2 = make< list<char> >(" --- ");
  j = find(list2.begin(), list2.end(), ' ');  
  k = find(++j, list2.end(), ' ');  // Find second blank.
  list1.splice(list1.begin(), list2, j, k);// Move the ---.
  assert (list1 == make< list<char> >("---Mark Twain"));
  assert (list2 == make< list<char> >("  "));
  return 0;
}
