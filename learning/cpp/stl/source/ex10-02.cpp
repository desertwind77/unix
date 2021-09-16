// Using find with normal and reverse iteration
#include <iostream>
#include <vector>
#include <algorithm> // for find
#include <iterator>
using namespace std;
template <typename Container>
Container make(const char s[])
{
  return Container(&s[0], &s[strlen(s)]);
}

int main()
{
  cout << "Using find with normal and reverse iteration:\n";
  vector<char> vector1 = 
      make< vector<char> >("now is the time");
  ostream_iterator<char> out(cout, " ");

  vector<char>::iterator i = 
    find(vector1.begin(), vector1.end(), 't');
  cout << "chars from the first t to the end: ";
  copy(i, vector1.end(), out); cout << endl;

  cout << "chars from the last t to the beginning: ";
  vector<char>::reverse_iterator r = 
    find(vector1.rbegin(), vector1.rend(), 't');
  copy(r, vector1.rend(), out); cout << endl;

  cout << "chars from the last t to the end: ";
  copy(r.base() - 1, vector1.end(), out); cout << endl;
  return 0;
}
