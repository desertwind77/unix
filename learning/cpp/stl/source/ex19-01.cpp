// First attempt at timing the sort algorithm
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main()
{
  cout << "First attempt at timing the sort algorithm."
       << endl;
  double* A, *B;
  unsigned long N;
  unsigned int reps;
  cout << "Input array size and repetitions: ";
  cin >> N >> reps;

  A = new double[N];
  B = new double[N];

  srand(time(0));

  for (unsigned int i = 0; i < N; ++i)
    A[i] = (double)rand();

  vector<long> iterations;
  iterations.reserve(reps);

  time_t start, finish;

  start = time(0);
  while (iterations.size() < reps) {
    int count = 0;
    do {
      ++count;
      copy(A, A + N, B);
      sort(B, B + N);
      finish = time(0);
    }
    // Continue as long as clock hasn't ticked:
    while (finish == start);
    // Record the number of iterations:
    iterations.push_back(count);
    start = finish;
  }
  cout << "Iteration counts: " << endl;
  unsigned int k;
  for (k = 0; k < iterations.size(); ++k) 
    cout << iterations[k] << " ";
  cout << endl;
  cout << "Sorted iteration counts: " << endl;
  sort(iterations.begin(), iterations.end());
  for (k = 0; k < iterations.size(); ++k) 
    cout << iterations[k] << " ";
  cout << endl;
  cout << "Selected value: " << iterations[reps/2] << endl;
  cout << "Time: " << 1000.0/iterations[reps/2]
       << " ms " << endl;
  return 0;
}
