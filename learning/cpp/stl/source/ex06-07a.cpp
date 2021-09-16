
#line 1718 "ch06.w"
// Demonstrating the STL vector front and erase operations.

#line 1722 "ch06.w"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

#line 1710 "ch06.w"
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}
#line 1726 "ch06.w"


int main() 
{
  cout << "Demonstrating STL vector front "
       << "and erase operations." << endl;
  vector<char> vector1 = make< vector<char> >("abcdefghij");
  
  cout << "Popping characters off the front produces: "; 

  while (vector1.size() > 0) {
    cout << vector1.front();
    vector1.erase(vector1.begin());
  }
  cout << endl;
  return 0;
}
