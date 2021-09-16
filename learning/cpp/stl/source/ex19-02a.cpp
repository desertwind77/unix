// Timing stable_sort on random vectors
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>
#include <algorithm>
#include "timer.h"
using namespace std;

int main()
{
  cout << "Timing stable_sort on random vectors." << endl;
  srand(time(0));
  vector<double> v, v0;
  unsigned long N, N1, N2;
  unsigned int reps;
  cout << "Repetitions, initial size, and final size: ";
  cin >> reps >> N1 >> N2;

  timer tim;

  for (N = N1; N <= N2; N *= 2) {
    v.clear(); 
    v.reserve(N);
    for (unsigned int i = 0; i < N; ++i)
      v.push_back((double)rand());

    v0 = v;   // save the input vector in v0

    // Compute the baseline time for N
    tim.start_baseline(reps);
    do { 
      // Include the vector assignment in baseline time
      v = v0;
    } while (tim.check());
    tim.report(false);

    tim.start(reps, N);
    do {
      v = v0;    // Restore the saved vector v0 into v
      stable_sort(v.begin(), v.end());
    }
    while (tim.check());
    tim.report(false);
  }
  return 0;
}
