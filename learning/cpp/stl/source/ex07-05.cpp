// Computing an inner product of tuples represented as vectors
#include <vector>
#include <iostream>
using namespace std; 

int main()
{
  cout << "Computing an inner product of tuples "
       << "represented as vectors." << endl;

  const long N = 600000; // Length of tuples x and y
  const long S = 10; // Sparseness factor

  cout << "\nInitializing..." << flush;
  vector<double> x(N), y(N);
  long k;
  for (k = 0; 3 * k * S < N; ++k) 
    x[3 * k * S] = 1.0;
  for (k = 0; 5 * k * S < N; ++k) 
    y[5 * k * S] = 1.0;

  cout << "\n\nComputing inner product by brute force: " 
       << flush;
  double sum = 0.0;
  for (k = 0; k < N; ++k)
    sum += x[k] * y[k];
    
  cout << sum << endl;
  return 0;
}
