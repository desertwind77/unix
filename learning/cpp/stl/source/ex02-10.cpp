// Demonstrating generic merge algorithm, merging parts of an
// array and a deque, putting the result into a list
#include <iostream>
#include <string>
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
  cout << "Demonstrating generic merge algorithm,\n"
       << "merging parts of an array and a deque, putting\n"
       << "the result into a list." << endl;
  char s[] = "acegikm";
  
  deque<char> deque1 = 
    make< deque<char> >("bdfhjlnopqrstuvwxyz");

  // Initialize list1 with 26 copies of the letter x:
  list<char> list1(26, 'x');

  // Merge first 5 letters in array s with first 10 in
  // deque1, putting result in list1:
  merge(&s[0], &s[5], deque1.begin(), deque1.begin() + 10,
        list1.begin());

  assert (list1 == 
            make< list<char> >("abcdefghijlnopqxxxxxxxxxxx"));
  cout << " --- Ok." << endl;
  return 0;
}
