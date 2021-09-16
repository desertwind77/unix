// Illustrating the generic find_if algorithm
#include <iostream>
#include <algorithm>
#include <cassert>
#include <vector>
using namespace std;

// Define a unary predicate object type: 
class GreaterThan50 {
 public:
  bool operator()(int x) const { return x > 50; }
};

int main()
{
  cout << "Illustrating the generic find_if algorithm." 
       << endl;
  // Create a vector with values 0, 1, 4, 9, 16, ..., 144:
  vector<int> vector1;
  for (int i = 0; i < 13; ++i)
    vector1.push_back(i * i);

  vector<int>::iterator where;
  where = find_if(vector1.begin(), vector1.end(),
                  GreaterThan50());

  assert (*where == 64);
  cout << " --- Ok." << endl;
  return 0;
}
