
#line 2746 "ch05.w"
// Illustrating the generic equal and mismatch algorithms.
// This is the modification of Example 5.8, in which the first call to
// equal is INCORRECT. It is incorrect since the end of the driver
// list is reached without finding a disagreement, causing
// dereferencing beyond the end of the list.

#line 2754 "ch05.w"
#include <iostream>
#include <cassert>
#include <algorithm>
#include <string>
#include <list>
#include <deque>
#include <vector>
using namespace std;

int main()
{
  cout << "Illustrating the generic equal "
       << "and mismatch algorithms." << endl;
  list<string> driver_list;
  vector<string> vec;
  deque<string> deq;

  driver_list.insert(driver_list.end(), "Clark");
  driver_list.insert(driver_list.end(), "Rindt");
  driver_list.insert(driver_list.end(), "Senna");

  vec.insert(vec.end(), "Clark");
  vec.insert(vec.end(), "Rindt");
  vec.insert(vec.end(), "Senna");
  vec.insert(vec.end(), "Berger");

  deq.insert(deq.end(), "Clark");
  deq.insert(deq.end(), "Berger");

  // Show that driver_list and the first 3 elements of
  // vec are equal in all corresponding positions:
  assert (equal(vec.begin(), vec.end(), driver_list.begin()));  // INCORRECT

  // Show that deq and the first 2 elements of driver_list
  // are not equal in all corresponding positions:
  assert (!equal(deq.begin(), deq.end(),
                 driver_list.begin()));

  // Find the corresponding positions in deq and driver_list
  // at which unequal elements first occur:
  pair<deque<string>::iterator, list<string>::iterator>
    pair1 = mismatch(deq.begin(), deq.end(),
                     driver_list.begin());

  if (pair1.first != deq.end())
    cout << "First disagreement in deq and driver_list:\n  "
         << *(pair1.first) << " and " << *(pair1.second)
         << endl;
  return 0;
}
