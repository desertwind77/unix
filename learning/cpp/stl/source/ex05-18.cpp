// Illustrating the generic swap algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic swap algorithm." << endl;
  int high = 250, low = 0;

  swap(high, low);

  assert (high == 0 && low  == 250);
  cout << " --- Ok." << endl;

  vector<int> vector1(100, 1), vector2(200, 2);

  swap(vector1, vector2);
  
  assert (vector1 == vector<int>(200, 2) &&
          vector2 == vector<int>(100, 1));
  return 0;
}
