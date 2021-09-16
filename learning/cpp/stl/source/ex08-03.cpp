// Using a function object for operation counting, first version
#include <iostream>
#include <iomanip>
#include <cassert>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;
template <typename T>
class less_with_count : public binary_function<T, T, bool> {
public:
  less_with_count() { }
  bool operator()(const T& x, const T& y) {
        ++counter;
        return x < y;
  }
  long report() const {return counter;}
  static long counter;
};

template <typename T>
long less_with_count<T>::counter = 0;

int main() 
{
  cout << "Using a function object for operation counting, "
       << "first version." << endl;
  const long N1 = 1000, N2 = 128000;
  for (long N = N1; N <= N2; N *= 2) { 
    vector<int> vector1;
    for (int k = 0; k < N; ++k) 
      vector1.push_back(k);
    random_shuffle(vector1.begin(), vector1.end());
    less_with_count<int> comp_counter;
    less_with_count<int>::counter = 0;
    sort(vector1.begin(), vector1.end(), comp_counter);
    cout << "Problem size " << setw(9) << N 
         << ",  comparisons performed: " 
         << setw(9) << comp_counter.report() << endl;
  }
  return 0;
}
