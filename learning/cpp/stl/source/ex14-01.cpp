// Finding all anagram groups in order of decreasing size
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <map>
#include <iterator>
using namespace std; 
#include "ps.h" // Definitions of PS, firstLess, firstEqual

typedef vector<PS>::const_iterator PSi;
typedef pair<PSi, PSi> PPS;

int main() {
  cout << "Anagram group finding program:\n"
       << "finds all anagram groups in a dictionary.\n\n" 
       << flush;

  cout << "First, enter the name of the file containing\n"
       << "the dictionary: " << flush;
  string dictionary_name; 
  cin >> dictionary_name;
  ifstream ifs(dictionary_name.c_str());
  if (!ifs.is_open()) {
    cout << "Eh? Could not open file named "
         << dictionary_name << endl;
    exit(1);
  }
  cout << "\nReading the dictionary ..." << flush;
  typedef istream_iterator<string> string_input;
   
  vector<PS> word_pairs;
  copy(string_input(ifs), string_input(), 
       back_inserter(word_pairs));
  cout << "\nSearching " << word_pairs.size() 
    << " words for anagram groups..." << flush;
  sort(word_pairs.begin(), word_pairs.end(), firstLess);

  typedef map<int, list<PPS>, greater<int> > map_1;
  map_1 groups;
  cout << "\n\nThe anagram groups are" << endl;
  PSi j = word_pairs.begin(), finis = word_pairs.end(), k;
  while (true) {
    j = adjacent_find(j, finis, firstEqual);
    if (j == finis) break;
    k = find_if(j + 1, finis, not1(bind1st(firstEqual, *j)));
    if (k-j > 1)
      // Save the positions j and k delimiting the anagram
      // group in the list of groups of size k-j:
      groups[k-j].push_back(PPS(j,k));
    j = k;
  }
  map_1::const_iterator m;
  for (m = groups.begin(); m != groups.end(); ++m) {
    cout << "\nAnagram groups of size " << m->first << ":\n";
    list<PPS>::const_iterator l;
    for (l = m->second.begin(); l != m->second.end(); ++l) {
      cout << "   ";
      j = l->first;  // beginning of the anagram group 
      k = l->second; // end of the anagram group
      copy(j, k, ostream_iterator<string>(cout, " "));
      cout << endl;
    }
  } 
  return 0;
}
