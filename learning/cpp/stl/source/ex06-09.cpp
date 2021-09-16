// Demonstrating the STL deque push_back and
// push_front functions
#include <iostream>
#include <cassert>
#include <string>
#include <deque>
#include <algorithm> // for reverse
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main() 
{
  deque<char> deque1 = 
                  make< deque<char> >("Bjarne Stroustrup"),
              deque2;
  deque<char>::iterator i;

  cout << "Demonstrating deque push_back function" << endl;
  for (i = deque1.begin(); i != deque1.end(); ++i)
    deque2.push_back(*i);
  assert (deque1 == deque2);
  
  deque1 = make< deque<char> >("Bjarne Stroustrup");
  deque2 = make< deque<char> >("");
   
  cout << "Demonstrating deque push_front function" << endl;
  for (i = deque1.begin(); i != deque1.end(); ++i)
    deque2.push_front(*i);
  assert (deque2 == make< deque<char> >("purtsuortS enrajB"));

  // Show that deque2 is the reverse of deque1 by using
  // STL generic reverse function to reverse deque1:
  reverse(deque1.begin(), deque1.end());
  assert (deque2 == deque1);
  cout << " --- Ok." << endl;
  return 0;
}
