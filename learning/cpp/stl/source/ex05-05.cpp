// Illustrating the generic adjacent_find algorithm
#include <iostream>
#include <string>
#include <algorithm>
#include <cassert>
#include <functional>
#include <deque>
using namespace std;

int main()
{
  cout << "Illustrating the generic adjacent_find algorithm." 
       << endl;
  deque<string> player(5);
  deque<string>::iterator i;

  // Initialize the deque:
  player[0] = "Pele";
  player[1] = "Platini";
  player[2] = "Maradona";
  player[3] = "Maradona";
  player[4] = "Rossi";

  // Find the first pair of equal consecutive names:
  i = adjacent_find(player.begin(), player.end());

  assert (*i == "Maradona" && *(i+1) == "Maradona");

  // Find the first name that is lexicographically
  // greater than the following name:
  i = adjacent_find(player.begin(), player.end(), 
                    greater<string>());

  assert (*i == "Platini" && *(i+1) == "Maradona");
  cout << " --- Ok." << endl;
  return 0;
}
