// Demonstrating the generic find algorithm with a vector
#include <iostream>
#include <cassert>
#include <vector>
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
       << "a vector." << endl;

  vector<char> vector1 = 
    make< vector<char> >("C++ is a better C");

  // Search for the first occurrence of the letter e:
  vector<char>::iterator
    where = find(vector1.begin(), vector1.end(), 'e');

  assert (*where == 'e' && *(where + 1) == 't');
  cout << " --- Ok." << endl;
  return 0;
}
