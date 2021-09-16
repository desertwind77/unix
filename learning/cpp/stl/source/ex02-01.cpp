// Using the STL generic reverse algorithm with a string and an array
#include <iostream>
#include <string>
#include <cassert> 
#include <algorithm> // For reverse algorithm
using namespace std;

int main()
{
  cout << "Using reverse algorithm with a string" << endl;
  string string1 = "mark twain";
  reverse(string1.begin(), string1.end());
  assert (string1 == "niawt kram");
  cout << " --- Ok." << endl;

  cout << "Using reverse algorithm with an array" << endl;
  char array1[] = "mark twain";
  int N1 = strlen(array1);
  reverse(&array1[0], &array1[N1]);
  assert (string(array1) == "niawt kram");
  cout << " --- Ok." << endl;
  return 0;
}
