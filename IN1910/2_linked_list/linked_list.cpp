#include <iostream>
#include <sstream>
#include <vector>
#include <stdexcept>
#include <math.h>
#include <assert.h>
using namespace std;

// Making a doubly linked list.

struct Node {
    int val;
    Node* next;
    Node* last;
    Node(int, Node*);
    Node(int, Node*, Node*);
};

Node::Node(int n, Node* L) {
    val = n;
    next = nullptr;
    last = L;
}

Node::Node(int n, Node* N, Node* L) {
    val = n;
    next = N;
    last = L;
}

class LinkedList {
    private:
        Node* head;
        Node* tail;
        int len;
    public:
        LinkedList();
        LinkedList(vector<int>);
        ~LinkedList();
        int length();
        void append(int);
        void insert(int, int);
        void remove(int);
        int& operator[](int);
        int pop(int);
        int pop();
        void print();
};

// Constructor
LinkedList::LinkedList() {
    head = nullptr;
    tail = nullptr;
    len = 0;
}

// Overloaded constructor
LinkedList::LinkedList(vector<int> init) {
    head = nullptr;
    tail = nullptr;
    len = 0;

    for (int i=0; i<init.size(); i++){
        append(init[i]);
    }
}

// Destructor
LinkedList::~LinkedList(){
    Node* index;
    Node* next;

    index = head;
    while (index != nullptr) {
        next = index->next;
        delete index;
        index = next;
    }
}

// Method that returns current length of list
int LinkedList::length() {
    return len;
}

// Method that appends elements to the list
void LinkedList::append(int e) {
    if (head == nullptr) {
        head = new Node(e, nullptr);
        tail = head;
        len += 1;
        return;
    }

    else {
        Node* index;
        index = head;

        while (index->next != nullptr) {
            index = index->next;
        }

        tail = new Node(e, index);
        index->next = tail;
        len += 1;
        return;
    }
}

// Method to insert elements in the list, at a given index
void LinkedList::insert(int val, int index) {
    if ((index < 0) && (index > len)) {
        string index_error = "Index ";
        index_error += to_string(index);
        index_error += " out of range.\n";
        throw out_of_range(index_error);
    }
    if (index == len) {
        append(val);
        return;
    }
    if (index == 0) {
        Node* old_head = head;
        Node* new_head;
        new_head = new Node(val, old_head, nullptr);
        old_head->last = new_head;
        head = new_head;
        len += 1;
        return;
    }
    else {
        Node* before = head;
        Node* after;
        for (int i=0; i<(index-1); i++) {
            before = before->next;
        }
        after = before->next;

        Node* new_node;
        new_node = new Node(val, after, before);
        after->last = new_node;
        before->next = new_node;
        len += 1;
        return;
    }
}

// Method to remove an element of the list, at a given index
void LinkedList::remove(int index) {
    if ((index < 0) || (index > len)) {
        string index_error = "Index ";
        index_error += to_string(index);
        index_error += " out of range.\n";
        throw out_of_range(index_error);
    }
    if (index == 0) {
        // Removes the first element, sets the head
        // correctly and sets head->last to a nullpointer
        Node* old_head = head;
        Node* new_head = head->next;
        new_head->last = nullptr;
        head = new_head;
        delete old_head;
        len -= 1;
        return;
    }
    if (index == len-1) {
        // Removes the last element, sets the tail
        // correctly and sets tail-> next to a nullpointer
        Node* old_tail = tail;
        Node* new_tail = tail->last;
        new_tail->next = nullptr;
        tail = new_tail;
        delete old_tail;
        len -= 1;
        return;

    }
    else {
        Node* before = head;
        Node* delete_node;
        Node* after;
        for (int i=0; i<(index-1); i++) {
            before = before->next;
        }
        delete_node = before->next;
        after = delete_node->next;

        before->next = after;
        after->last = before;
        delete delete_node;
        len -= 1;
        return;
    }
}

// Operator that returns the value of an index
int& LinkedList::operator[](int n) {
    if ((n < 0) && (n >= len)) {
        string index_error = "Index ";
        index_error += to_string(n);
        index_error += " out of range.\n";
        throw out_of_range(index_error);
    }

    Node* index = head;
    for (int i=0; i<n; i++) {
        index = index->next;
    }
    return index->val;
}

// Method for returning and removing the indexed element
int LinkedList::pop(int index) {
    int val = operator[](index);
    remove(index);
    return val;
}

// Method for returning and removing the last element
int LinkedList::pop() {
    int val = operator[](len-1);
    remove(len-1);
    return val;
}

// Method that prints elements in the list
void LinkedList::print() {
    Node* index = head;
    cout << "[";
    while (index->next != nullptr) {
        cout << index->val << ", ";
        index = index->next;
    }
    cout << index->val << "]" << endl;
}

// Test for LinkedList
void test_LinkedList(int N) {
    for (int n=0; n<N; n++) {
        vector<int> test_list = {1,2,3,4,5,6,7,8,9};
        vector<int> test_check1 = {1,3,5,7,9};
        vector<int> test_check2 = {-1,1,3,5,7,9,11};

        LinkedList test_LinkedList(test_list);
        assert(test_LinkedList.length() == 9);
        for (int i=0; i<test_list.size(); i++) {
            assert(test_list[i] == test_LinkedList[i]);
        }
        int a = test_LinkedList.pop(1);
        int b = test_LinkedList.pop(2);
        int c = test_LinkedList.pop(3);
        int d = test_LinkedList.pop(4);
        assert(a == 2);
        assert(b == 4);
        assert(c == 6);
        assert(d == 8);

        for (int i=0; i<test_LinkedList.length(); i++) {
            assert(test_check1[i] == test_LinkedList[i]);
        }
        test_LinkedList.insert(-1, 0);
        test_LinkedList.append(11);

        for (int i=0; i<test_LinkedList.length(); i++) {
            assert(test_check2[i] == test_LinkedList[i]);
        }

        // Checking that pop() gets the last value.
        int e = test_LinkedList.pop();
        assert(e == 11);

        int f = 42;
        test_LinkedList[0] = f;
        test_LinkedList[2] = f;
        test_LinkedList[4] = f;
        assert(f == test_LinkedList[0]);
        assert(f == test_LinkedList[2]);
        assert(f == test_LinkedList[4]);
        test_LinkedList[0] = -1;
        test_LinkedList[2] = 3;
        test_LinkedList[4] = 7;

        test_LinkedList.insert(f,1);
        test_LinkedList.insert(f,3);
        test_LinkedList.insert(f,7);
        assert(test_LinkedList[1] == f);
        assert(test_LinkedList[3] == f);
        assert(test_LinkedList[7] == f);
    }
}

int main() {

    test_LinkedList(10);

    LinkedList init; // Constructor
    for (int i=1; i<12; i++) {
        init.append(i*(i+1));
    }
    cout << "List 1: ";
    init.print(); // void print();

    int L = init.length(); // int length();
    cout << "List has " << L << " elements." << endl << endl;

    // Removes every other element in the list from the back
    for (int i=L-1; i>=0; i-=2) {
        init.remove(i); // void remove(int);
    }
    cout << "List 1 with every other element removed: ";
    init.print();

    int L_2 = init.length();
    cout << "New length is: " << L_2 << "." << endl << endl;

    // Inserts new elements to every other list from the front
    for (int i=0; i<=L_2*2; i+=2) {
        init.insert((i+1)*(i+3), i); // void insert(int, int);
    }
    cout << "List 1 with new elements added: ";
    init.print();

    int L_3 = init.length();
    cout << "New length is: " << L_3 << "." << endl << endl;

    // New list initialised with elements.
    vector<int> victor = {2, 3, 5, 7, 11, 13};
    LinkedList init2 (victor); // Overloaded constructor

    cout << "List 2: ";
    init2.print();

    int L_4 = init2.length();
    int array[9] = {17, 19, 23, 23, 29, 31, 37, 41, 43};

    // Appending new primes to list
    for (int p: array) {
      init2.append(p); // void append(int);
    }

    cout << endl << "List 2 with values appended: ";
    init2.print();

    int v1 = init2[8]; // Operator
    int v2 = init2.pop(9); // int pop(int)
    int v3 = init2.pop(); // int pop()

    cout << endl << "Element " << v1 << " appears twice in list."
    << endl << "List 2 with " << v2 << " and last value (" << v3 << ") popped: ";
    init2.print();

    return 0;
}
