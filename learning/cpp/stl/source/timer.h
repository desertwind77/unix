// Define a timer class for analyzing algorithm performance.
#include <iostream>
#include <iomanip>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

class timer {
public:
  timer();  // Default constructor
  // Start a series of r trials for problem size N:
  void start(unsigned int r, unsigned long N);
  // Start a series of r trials to determine baseline time:
  void start_baseline(unsigned int r);
  // Returns true if the trials have been completed, else false
  bool check();
  // Report the results of the trials on cout
  // with additional output if verbose is true:
  void report(bool verbose);
  // Returns the results for external use
  const map<unsigned int, double>& results() const;

private:
  unsigned int reps;  // Number of trials
  // For storing loop iterations of a trial
  vector<long> iterations;
  // For saving initial and final times of a trial
  time_t initial, final;
  // For counting loop iterations of a trial
  unsigned long count;
  // For saving the problem size (N) for current trials
  unsigned int problem_size;
  // For storing (problem size, time) pairs
  map<unsigned int, double> result_map;
  // true if this is a baseline computation, false otherwise
  bool baseline;
  // For recording the baseline time 
  double baseline_time;
};

timer::timer() { baseline = false; }
void timer::start(unsigned int r, unsigned long N) 
{
  reps = r;
  problem_size = N;
  count = 0;
  iterations.clear();
  iterations.reserve(reps);
  initial = time(0);
}
void timer::start_baseline(unsigned int r) 
{
  baseline = true;
  start(r, 0);
}
bool timer::check() 
{
  ++count;
  final = time(0);
  if (initial < final) {
    iterations.push_back(count);  
    initial = final;
    count = 0;
  }
  return (iterations.size() < reps);
}
void timer::report(bool verbose)
{
  if (verbose) {
    for (unsigned int k = 0; k < iterations.size(); ++k) {
      cout << iterations[k] << " ";
      if ((k+1) % 10 == 0)
        cout << endl;
    }
    cout << endl;
  }
  sort(iterations.begin(), iterations.end());
  if (verbose) {
    cout << "Sorted counts:" << endl;
    for (unsigned int k = 0; k < iterations.size(); ++k) {
      cout << iterations[k] << " ";
      if ((k+1) % 10 == 0)
        cout << endl;
    }
    cout << endl;
  }

  int selected_count = iterations[reps/2];
  if (verbose) 
    cout << "Selected count: " << selected_count << endl;

  if (baseline) {
    baseline_time = 1000.0/selected_count;
    cout << "Baseline time: " << baseline_time << endl;
    baseline = false;
  } else {
    double calculated_time, growth_factor;
    result_map[problem_size] = calculated_time = 
      1000.0/selected_count - baseline_time;
    cout << setiosflags(ios::fixed) << setprecision(4)
         << setw(35) << problem_size << setw(12)
         << calculated_time << " ms ";
    if (result_map.find(problem_size/2) != result_map.end()) {
      growth_factor = calculated_time / result_map[problem_size/2];
      cout << setiosflags(ios::fixed) << setprecision(4) 
           << setw(8) << growth_factor;
    }
    cout << endl;
  }
}
const map<unsigned int, double>& timer::results() const
{
  return result_map;
}
