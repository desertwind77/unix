// Demonstrating the generic merge algorithm with an array, a
// list, and a deque
#include <iostream>
#include <cassert>
#include <list>
#include <deque>
#include <algorithm>  // For merge
using namespace std; 
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main()
{
  cout << "Demonstrating generic merge algorithm with "
       << "an array, a list, and a deque." << endl;
  char s[] = "aeiou";
  int len = strlen(s);
  list<char> list1 = 
     make< list<char> >("bcdfghjklmnpqrstvwxyz");

  // Initialize deque1 with 26 copies of the letter x:
  deque<char> deque1(26, 'x');

  // Merge array s and list1, putting result in deque1:
  merge(&s[0], &s[len], list1.begin(), list1.end(),
        deque1.begin());
  assert (deque1 == 
            make< deque<char> >("abcdefghijklmnopqrstuvwxyz"));
  cout << " --- Ok." << endl;
  return 0;
}
