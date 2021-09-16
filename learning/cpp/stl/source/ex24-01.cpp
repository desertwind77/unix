// Demonstrating use of a custom allocator
#include <iostream>
#include <vector>
using namespace std;

#include "logalloc.h"

int main()
{
  cout << "Demonstrating use of a custom allocator." << endl;

  cout << "-- Default allocator --" << endl;
  vector<int> v1;
  for (int i = 0; i < 10; ++i) {
    cout << "    Inserting " << i << endl;
    v1.push_back(i);
  }
  cout << "-- Done. --" << endl;

  cout << "\n-- Custom allocator --" << endl;
  vector<int, logging_allocator<int> > v2;
  for (int i = 0; i < 10; ++i) {
    cout << "    Inserting " << i << endl;
    v2.push_back(i);
  }
  cout << "-- Done. --" << endl;

  cout << "\n-- Custom allocator with reserve --" << endl;
  vector<int, logging_allocator<int> > v3;
  v3.reserve(10);
  for (int i = 0; i < 10; ++i) {
    cout << "    Inserting " << i << endl;
    v3.push_back(i);
  }
  cout << "-- Done. --" << endl;

  return 0;
}
