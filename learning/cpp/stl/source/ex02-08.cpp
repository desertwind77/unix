// Demonstrating the generic find algorithm with a deque
#include <iostream>
#include <cassert>
#include <deque>
#include <algorithm>  // For find
using namespace std; 
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}
  
int main()
{
  cout << "Demonstrating generic find algorithm with "
       << "a deque." << endl;
  deque<char> deque1 = 
    make< deque<char> >("C++ is a better C");

  // Search for the first occurrence of the letter e:
  deque<char>::iterator
    where = find(deque1.begin(), deque1.end(), 'e');
  assert (*where == 'e' && *(where + 1) == 't');
  cout << " --- Ok." << endl;
  return 0;
}
