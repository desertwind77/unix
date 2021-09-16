// Illustrating the random_shuffle algorithm
#include <algorithm>
#include <vector>
#include <functional>  
#include <iostream>
#include <iterator>
using namespace std;

int main() {
  cout << "Illustrating the random_shuffle algorithm." << endl;
  const int N = 20;
  vector<int> vector1(N);
  for (int i = 0; i < N; ++i) 
    vector1[i] = i;

  for (int j = 0; j < 3; ++j) {
    // Randomly shuffle the integers in vector1:
    random_shuffle(vector1.begin(), vector1.end()); 

    // Output the contents of vector1:
    copy(vector1.begin(), vector1.end(),
         ostream_iterator<int>(cout, " "));
    cout << endl;
  }
  return 0;
}
