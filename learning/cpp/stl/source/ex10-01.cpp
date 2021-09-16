// Illustrating normal and reverse iteration.
#include <iostream>
#include <vector>
#include <list>
using namespace std;

template <typename Container>
void display(const Container& c) 
{

  cout << "Elements in normal (forward) order:  ";
  typename Container::const_iterator i;
  for (i = c.begin(); i != c.end(); ++i) 
     cout << *i << "  ";
  cout << endl;

  cout << "Elements in reverse order:           ";
  typename Container::const_reverse_iterator r;
  for (r = c.rbegin(); r != c.rend(); ++r) 
     cout << *r << "  ";
  cout << endl;
}

int main()
{
  cout << "Normal and reverse iteration through a vector:\n";
  vector<int> vector1;
  vector1.push_back(2);
  vector1.push_back(3);
  vector1.push_back(5);
  vector1.push_back(7);
  vector1.push_back(11);

  display(vector1);

  cout << "Normal and reverse iteration through a list:\n";
  list<int> list1(vector1.begin(), vector1.end());

  display(list1);
  return 0;
}
