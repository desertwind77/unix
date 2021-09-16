// Illustrating the generic search algorithm
#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>
#include <deque>
using namespace std;

int main()
{
  cout << "Illustrating the generic search algorithm." << endl;
  vector<int> vector1(20);
  deque<int>  deque1(5);
  // Initialize vector1 with 0, 1, ..., 19:
  int i;
  for (i = 0; i < 20; ++i) 
    vector1[i] = i;

  // Initialize deque1 with 5, 6, 7, 8, 9:
  for (i = 0; i < 5; ++i) 
    deque1[i] = i + 5;

  // Search for first occurrence of deque1's contents 
  // as a subsequence of the vector contents:
  vector<int>::iterator k = 
    search(vector1.begin(), vector1.end(), 
           deque1.begin(), deque1.end());

  // Verify that 5, 6, 7, 8, 9 occur in vector1 
  //    starting at the position to which k refers:
  for (i = 0; i < 5; ++i) 
    assert (*(k + i) == i + 5);
  cout << " --- Ok." << endl;
  return 0;
}
