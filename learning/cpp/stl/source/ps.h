// Define a structure, PS, and some related functions for holding 
// pairs of strings
#include <functional>
using namespace std;
struct PS : pair<string, string> {
  PS() : pair<string, string>(string(), string()) { }
  PS(const string& s) : pair<string, string>(s, s) {
    sort(first.begin(), first.end());
  }
  operator string() const { return second; }
};
struct FirstLess : binary_function<PS, PS, bool> {
  bool operator()(const PS& p, const PS& q) const 
  { 
    return p.first < q.first; 
  }
} firstLess;
struct FirstEqual : binary_function<PS, PS, bool> {
  bool operator()(const PS& p, const PS& q) const 
  { 
    return p.first == q.first; 
  }
} firstEqual;
