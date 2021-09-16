// Finding all anagram groups in a given dictionary of words
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include <map>
#include <iterator>
#include <functional>
using namespace std;

typedef multimap<string, string> multimap_1;
typedef multimap_1::value_type PS;
typedef multimap_1::const_iterator PSi;
 
typedef pair<PSi, PSi> PPS;
 
int main() {
  cout << "Anagram group finding program:\n"
    << "finds all anagram groups in a dictionary.\n\n";
 
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
 
  // Copy words from dictionary file to 
  // a multimap:
  typedef istream_iterator<string> string_input;
  multimap_1 word_pairs;
  for (string_input in(ifs); in != string_input(); ++in) {
    string word = *in;
    sort(word.begin(), word.end());
    word_pairs.insert(PS(word, *in));
  } 
 
  cout << "\nSearching " << word_pairs.size() 
    << " words for anagram groups..." << flush;
 
  // Set up the map from anagram group sizes to lists of
  // groups of that size:
  typedef map<int, list<PPS>, greater<int> > map_1;
  map_1 groups;
 
  // Find all the anagram groups and save their 
  // positions in the groups map:
  cout << "\n\nThe anagram groups are: " << endl;
  PSi j = word_pairs.begin(), finis = word_pairs.end(), k;
  while (true) {
    // Make j point to the next anagram 
    // group, or to the end of the multimap:
    j = adjacent_find(j, finis,
                      not2(word_pairs.value_comp()));
    if (j == finis) break;
    
    k = find_if(j, finis, 
                bind1st(word_pairs.value_comp(), *j));
    multimap_1::size_type n = distance(j, k);
    if (n > 1)
      // Save the positions j and k delimiting the anagram
      // group in the list of groups of size n:
      groups[n].push_back(PPS(j, k)); 
 
    // Prepare to continue search at position k:
    j = k;
  }
 
  // Iterate through the groups map to output the anagram
  // groups in order of decreasing size:
  map_1::const_iterator m;
  for (m = groups.begin(); m != groups.end(); ++m) {
 
    cout << "\nAnagram groups of size "
      << m->first << ":\n";
 
    list<PPS>::const_iterator l;
    for (l = m->second.begin(); 
         l != m->second.end(); ++l) {
      cout << "   ";
      j = l->first;  // Beginning of the anagram group 
      k = l->second; // End of the anagram group
      for (; j != k; ++j)
        cout << j->second << " ";
      cout << endl;
    }
  }
  return 0;
}
