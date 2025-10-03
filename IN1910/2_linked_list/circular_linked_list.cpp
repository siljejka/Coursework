#include <iostream>
#include <stdexcept>
#include <vector>
#include <ctime>
#include <assert.h>
using namespace std;


struct Node {
    int val;
    Node* next;
    Node(int);
    Node(int, Node*);
};

Node::Node(int n) {
    val = n;
    next = nullptr;
}

Node::Node(int n, Node* N) {
    val = n;
    next = N;
}

class CircLinkedList {
    private:
        Node* head;
        Node* tail;
        int len;
    public:
        CircLinkedList();
        CircLinkedList(int);
        ~CircLinkedList();
        int length();
        void append(int);
        int& operator[](int);
        void print();
        vector<int> josephus_sequence(int);
};

// Constructor
CircLinkedList::CircLinkedList() {
    head = nullptr;
    tail = nullptr;
    len = 0;
}

// Overload Constructor
CircLinkedList::CircLinkedList(int n) {
    head = nullptr;
    tail = nullptr;
    len = 0;
    for (int i=1; i<(n+1); i++) {
        append(i);
    }
}

// Destructor
CircLinkedList::~CircLinkedList(){
    if (len == 0) {
        return;
    }
    if (len == 1) {
        delete head;
        return;
    }
    else {
        Node* index;
        Node* next;

        index = head;
        while (index != tail) {
          next = index->next;
          delete index;
          index = next;
        }
        delete index;
    }
}

// Method that returns current length of list
int CircLinkedList::length() {
    return len;
}

// Method that appends elements to the list
void CircLinkedList::append(int e) {
    if (head == nullptr) {
        head = new Node(e);
        head->next = head;
        tail = head;
        len += 1;
        return;
    }
    else {
        Node* index;
        index = head;

        while (index->next != head) {
            index = index->next;
        }

        tail = new Node(e, head);
        index->next = tail;
        len += 1;
        return;
    }
}

// Operator that returns the value of an index
int& CircLinkedList::operator[](int n) {
    if (len == 0) {
        throw range_error("Error: List is empty");
    }
    else {
        Node* index = head;
        for (int i=0; i<n; i++) {
            index = index->next;
        }
        return index->val;
    }
}

// Method for printing the list in order
void CircLinkedList::print() {
      if (len == 0){
          return;
      }
      if (len == 1){
          cout << "[" << head->val << "]" << endl;
          return;
      }
      else {
          Node* index = head;
          cout << "[";
          while (index->next != head) {
              cout << index->val << ", ";
              index = index->next;
          }
          cout << tail->val << "]" << endl;
      }
}

// Method for removing every kth item in list
vector<int> CircLinkedList::josephus_sequence(int k) {
    vector<int> victor;
    victor.resize(len);

    if (k == 1) {
        for (int i=0; i<len; i++) {
            victor[i] = i+1;
        }
        return victor;
    }
    else {
        int count = 0;
        Node* index = head;
        Node* victim;

        while (len > 1) {
          for (int i=0; i<(k-2); i++){
            index = index->next;
          }
          victim = index->next;
          victor[count] = victim->val;
          index->next = victim->next;

          index = victim->next;
          delete victim;

          len -= 1;
          count += 1;
        }
        victor[count] = index->val;
        len -=1;
        delete index;

        return victor;
    }
}

// Initialises the class with n people where every kth person is killed
int last_man_standing(int n, int k) {
    CircLinkedList potential_victims(n);
    vector<int> ordered_victims = potential_victims.josephus_sequence(k);
    return ordered_victims[n-1];
}

void expected_values_test() {
    vector<int> n_3th = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
    vector<int> expected_3th = {2, 1, 4, 1, 4, 7, 1, 4, 7, 10};

    vector<int> n_4th = {4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
    vector<int> expected_4th = {2, 1, 5, 2, 6, 1, 5, 9, 1, 5};

    vector<int> n_5th = {5, 6, 7, 8, 9, 10, 11, 12, 13, 14};
    vector<int> expected_5th = {2, 1, 6, 3, 8, 3, 8, 1, 6, 11};

    for (int i=0; i<10; i++) {
        bool v1 = expected_3th[i] == last_man_standing(n_3th[i], 3);
        bool v2 = expected_4th[i] == last_man_standing(n_4th[i], 4);
        bool v3 = expected_5th[i] == last_man_standing(n_5th[i], 5);
        assert(v1 == true);
        assert(v2 == true);
        assert(v3 == true);
    }
}

// Returns the expected value for n people where every 2nd person is killed
int josephus_expected(int n) {
    int i = 1;
    while (n > i) {
        i *= 2;
    }
    if (n==i) {
        return 1;
    }
    else {
        i /= 2;
        int l = n-i;
        int last_victor = (2*l) + 1;
        return last_victor;
    }
}

// Runs N tests with random n values, test for k=2, since we can get the
// survivor from josephus_expected if k=2.
// The random value generator is initalised with a seed based on the current
// UNIX time
void randomised_values_test(int N) {
    int n_max = 200;
    int n_min = 1;
    int* n_vals = new int[N];
    int n;
    srand(time(0));
    for (int i=0; i<N; i++) {
        n_vals[i] = rand() % n_max + n_min;
    }

    for (int i=0; i<N; i++) {
        n = n_vals[i];
        int exp_winner = josephus_expected(n);
        int calc_winner = last_man_standing(n,2);
        bool calc_correct = (exp_winner == calc_winner);
        assert(calc_correct == true);
    }
}

int main() {
    expected_values_test();
    randomised_values_test(1000);

    int task_4g = last_man_standing(68, 7);
    cout << task_4g << endl;

    return 0;
}
