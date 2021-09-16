// Illustrating the priority_queue adaptor.
#include <iostream>
#include <queue> // Defines both queue and priority_queue
using namespace std;

int main()
{
  cout << "Illustrating the priority_queue adaptor." << endl;
  int thedata[] = {45, 34, 56, 27, 71, 50, 62};
  priority_queue<int> pq;  
  cout << "The priority_queue size is now " << pq.size() 
       << endl;
  int i;
  cout << "Pushing 4 elements " << endl;
  for (i = 0; i < 4; ++i)
    pq.push(thedata[i]);
  cout << "The priority_queue size is now " << pq.size() 
       << endl;
  cout << "Popping 3 elements " << endl;
  for (i = 0; i < 3; ++i) {
    cout << pq.top() << endl;
    pq.pop();
  }
  cout << "The priority_queue size is now " << pq.size() 
       << endl;
  cout << "Pushing 3 elements " << endl;
  for(i = 4; i < 7; ++i)
    pq.push(thedata[i]);
  cout << "The priority_queue size is now " << pq.size() 
       << endl;
  cout << "Popping all elements" << endl;
  while (!pq.empty()) {
    cout << pq.top() << endl;
    pq.pop();
  } 
  cout << "The priority_queue size is now " << pq.size() 
       << endl;
  return 0;
}
