// Demonstrating an STL map
#include <iostream>
#include <map>
#include <string>
using namespace std; 

int main()
{
  map<string, long> directory;
  directory["Bogart"] = 1234567;
  directory["Bacall"] = 9876543;
  directory["Cagney"] = 3459876;
  // And so on

  // Read some names and look up their numbers:
  string name;
  while (cin >> name) 
    if (directory.find(name) != directory.end()) 
      cout << "The phone number for " << name
           << " is " << directory[name] << "\n";
    else
      cout << "Sorry, no listing for " << name << "\n";
  return 0;
}
