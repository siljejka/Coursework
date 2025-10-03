#include <iostream>
#include <vector>
#include <stdexcept>
#include <ctime>
#include <cmath>
#include <assert.h>
using namespace std;


struct Node {
    int val;
    Node* next;
    Node* last;
    Node(int);
    Node(int, Node*);
    Node(int, Node*, Node*);
};

Node::Node(int n) {
    val = n;
    next = nullptr;
    last = nullptr;
}

Node::Node(int n, Node* N) {
    val = n;
    next = N;
    last = nullptr;
}

Node::Node(int n, Node* N, Node* L) {
    val = n;
    next = N;
    last = L;
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
        void remove_node(Node*);
        vector<int> josephus_sequence(int);
        int pop(Node*);
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
        return;
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
        head->last = head;
        tail = head;
        len += 1;
        return;
    }
    else {
        Node* index;
        Node* before_last;
        index = head;

        while (index->next != head) {
            index = index->next;
        }
        before_last = index->last;
        tail = new Node(e, head, index);
        before_last->next = index;
        head->last = tail;
        index->next = tail;
        len += 1;
        return;
    }
}

int& CircLinkedList::operator[](int n) {
    if (len == 0) {
        throw range_error("Error: List is empty");
    }
    if (n<0) {
        Node* index = head;
        for (int i=-1; i>(n-1); i--) {
            index = index->last;
        }
        return index->val;
    }
    else {
        Node* index = head;
        for (int i=0; i<n; i++) {
            index = index-> next;
        }
        return index->val;
    }
}

void CircLinkedList::print() {
    if (len == 0) {
        cout << "[]" << endl;
    }
    Node* index = head;
    cout << "[";
    while (index->next != head) {
        cout << index-> val << ", ";
        index = index-> next;
    }
    cout << tail->val << "]" << endl;
}

void CircLinkedList::remove_node(Node* delete_node) {
  if (len == 0) {
      throw range_error("Error: List is empty");
  }
  if (delete_node == head) {
      head = delete_node->next;
      tail->next = head;
      head->last = tail;
      delete delete_node;
      len -= 1;
      return;
  }
  if (delete_node == tail) {
      tail = delete_node->last;
      tail->next = head;
      head->last = tail;
      delete delete_node;
      len -= 1;
      return;
  }
  else {
      Node* before = delete_node->last;
      Node* after = delete_node->next;
      before->next = after;
      after->last = before;
      delete delete_node;
      len -= 1;
      return;
  }
}

int CircLinkedList::pop(Node* pop_node) {
    int val = pop_node->val;
    remove_node(pop_node);
    return val;
}


// Josephus Sequence method
vector<int> CircLinkedList::josephus_sequence(int k) {
    if (k == 0) {
        throw invalid_argument("k can not be 0.");
    }
    vector<int> jos_seq;
    jos_seq.resize(len);
    if (k==1) {
        for (int i=0; i<len; i++) {
            jos_seq[i] = i;
        }
        return jos_seq;
    }
    if (k==-1) {
      for (int i=len; i>0; i--) {
          jos_seq[i] = i;
      }
      return jos_seq;
    }
    else {
        int count = 0;
        Node* index = head;

        if (k > 0) {
            for (int i=0; i<(k-1); i++) {
                index = index->next;
            }
            while (len > 1) {
                jos_seq[count] = pop(index);
                index = index->next;
                for (int i=0; i<(k-1); i++) {
                    index = index->next;
                }
                count += 1;
            }
        }
        if (k < 0) {
          for (int i=0; i>(k+1); i--) {
              index = index->last;
          }
          while (len > 1) {
              jos_seq[count] = pop(index);
              index = index->last;
              for (int i=0; i>(k+1); i--) {
                  index = index->last;
              }
              count += 1;
          }
        }
        jos_seq[count] = index->val;
        delete index;
        len -= 1;
        return jos_seq;
    }
}

int last_man_standing(int n, int k) {
    CircLinkedList potential_victims(n);
    vector<int> ordered_victims = potential_victims.josephus_sequence(k);
    return ordered_victims[n-1];
}

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
        int win = (2*l) + 1;
        return win;
    }
}

void test_class(int N) {
    int n_max = 1000;
    int n_min = 1;
    int n_vals[N];
    srand(time(0));
    for (int i=0; i<N; i++) {
        n_vals[i] = rand() % n_max + n_min;
    }

    for (int n: n_vals) {
        int exp_winner = josephus_expected(n);
        int calc_winner = last_man_standing(n,2);
        bool calc_correct = (exp_winner == calc_winner);
        assert(calc_correct==true);
    }
}


int main() {
    int N = pow(10,3);
    test_class(N);

    int task_4g = last_man_standing(68, 7);
    cout << task_4g << endl;

    return 0;
}
