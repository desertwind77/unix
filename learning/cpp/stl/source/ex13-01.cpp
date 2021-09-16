// Find all anagram groups in a dictionary, and print them to
// standard output stream
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <iterator>
using namespace std; 
#include "ps.h" // Definitions of PS, firstLess, firstEqual

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
  vector<PS>::const_iterator j = word_pairs.begin(),
                             finis = word_pairs.end(), k;
  cout << "\n\nThe anagram groups are:" << endl;
  while (true) {
    j = adjacent_find(j, finis, firstEqual);
    if (j == finis) break;
    k = find_if(j + 1, finis, not1(bind1st(firstEqual, *j)));
    cout << "  ";
    copy(j, k, ostream_iterator<string>(cout, " "));
    cout << endl;
    j = k;
  }
  return 0;     
}
