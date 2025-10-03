#include <iostream>
#include <sstream>
#include <vector>
#include <stdexcept>
#include <math.h>
#include <assert.h>
using namespace std;


class ArrayList {
    private:
        int *particulars;
        int capacity;
        int len;
        int growth_factor;
    public:
        ArrayList();
        ArrayList(vector<int>);
        ~ArrayList();
        int length();
        int cap();
        void append(int);
        void insert(int, int);
        void remove(int);
        void resize();
        void shrink_to_fit();
        int& operator[](int);
        int pop(int);
        int pop();
        void print();
};

// Constructor
ArrayList::ArrayList() {
    len = 0;
    capacity = 1;
    growth_factor = 2;
    particulars = new int[capacity];
}

// Overloaded constructor
ArrayList::ArrayList(vector<int> init) {
    len = 0;
    capacity = 1;
    growth_factor = 2;
    particulars = new int[capacity];

    for (int i=0; i<init.size(); i++){
        append(init[i]);
    }
}

// Destructor
ArrayList::~ArrayList() {
    delete[] particulars;
}

// Method for current length of array
int ArrayList::length() {
    return len;
}

// Method for returning current capacity
int ArrayList::cap() {
    return capacity;
}

// Method for appending items to the array
void ArrayList::append(int n) {
    if (len >= capacity) {
        resize();
    }
    particulars[len] = n;
    len += 1;
}

// Method for inserting values in the array
void ArrayList::insert(int val, int index) {
    if ((index < 0) || (index > len)) {
        string index_error = "Index ";
        index_error += to_string(index);
        index_error += " out of range.\n";
        throw out_of_range(index_error);
    }
    if (len >= capacity) {
        resize();
    }

    len += 1;

    for (int i=len; i>index; i--) {
        particulars[i] = particulars[i-1];
    }
    particulars[index] = val;
}

// Method for removing an element from the array
void ArrayList::remove(int index) {
    if ((index < 0) || (index > len)) {
        string index_error = "Index ";
        index_error += to_string(index);
        index_error += " out of range.\n";
        throw out_of_range(index_error);
    }

    len -= 1;

    for (int i=index; i<len; i++) {
        particulars[i] = particulars[i+1];
    }

    shrink_to_fit();
}

// Method for resizing array when it reaches max capacity
void ArrayList::resize() {
    capacity *= growth_factor;
    int *temp_particulars = new int[capacity];
    for (int i=0; i<len; i++) {
        temp_particulars[i] = particulars[i];
    }
    delete[] particulars;
    particulars = temp_particulars;
}

// Method for reducing capacity to fit array
void ArrayList::shrink_to_fit() {
    if (len <= (capacity/4)) {
        int new_capacity = 1;
        while (new_capacity < len) {
            new_capacity *= growth_factor;
        }

        capacity = new_capacity;
        int *temp_particulars = new int[capacity];
        for (int i=0; i<len; i++) {
            temp_particulars[i] = particulars[i];
        }
        delete[] particulars;
        particulars = temp_particulars;
    }
    else {}
}

// Operator that returns the value of an index
int& ArrayList::operator[](int n) {
    if ((0 <= n) && (n < len)) {
        return particulars[n];
    }
    else {
        string index_error = "Index ";
        index_error += to_string(n);
        index_error += " out of range.\n";
        throw out_of_range(index_error);
    }
}

// Method for returning and removing the indexed element
int ArrayList::pop(int index) {
    int val = operator[](index);
    remove(index);

    return val;
}

// Method for returning and removing the last element
int ArrayList::pop() {
    int val = operator[](len-1);
    remove(len-1);

    return val;
}

// Method for printing the list in order
void ArrayList::print() {
    /*Using stringstream because it allows us to change the code to return
    string instead if desired.*/
    stringstream list_str;

    list_str << "[";
    for (int i=0; i<(len-1); i++) {
        list_str << particulars[i] << ", ";
    }
    list_str << particulars[len-1] << "]";

    cout << list_str.str() << endl;
}

// Method to check if an integer is prime
bool is_prime(int n) {
    if (n == 1) {
        return false;
    }
    if (n == 2) {
      return true;
    }
    if (n%2 == 0) {
        return false;
    }

    int max_div;
    max_div = floor(sqrt(n));

    for (int d=3; d<n; d+=2) {
        if (n % d == 0) {
            return false;
        }
    }
    return true;
}

// Method to find the first n primes
void first_n_primes(int n) {
    ArrayList primes;
    int current_number = 1;
    bool is_current_prime = false;

    for (int i=0; i<n; i++) {
        while (is_current_prime == false) {
            current_number += 1;
            is_current_prime = is_prime(current_number);
        }
        primes.append(current_number);
        is_current_prime = false;
    }
    primes.print();
}

// Test for arraylist
void test_arraylist(int N) {
    for (int n=0; n<N; n++) {
        vector<int> test_list = {1,2,3,4,5,6,7,8,9};
        vector<int> test_check1 = {1,3,5,7,9};
        vector<int> test_check2 = {-1,1,3,5,7,9,11};

        ArrayList test_array(test_list);
        assert(test_array.length() == 9);
        for (int i=0; i<test_list.size(); i++) {
            assert(test_list[i] == test_array[i]);
        }
        int a = test_array.pop(1);
        int b = test_array.pop(2);
        int c = test_array.pop(3);
        int d = test_array.pop(4);
        assert(a == 2);
        assert(b == 4);
        assert(c == 6);
        assert(d == 8);

        for (int i=0; i<test_array.length(); i++) {
            assert(test_check1[i] == test_array[i]);
        }
        test_array.insert(-1, 0);
        test_array.append(11);

        for (int i=0; i<test_array.length(); i++) {
            assert(test_check2[i] == test_array[i]);
        }

        // Checking that pop() gets the last value.
        int e = test_array.pop();
        assert(e == 11);

        int f = 42;
        test_array[0] = f;
        assert(f == test_array[0]);

        ArrayList check_sizing;
        assert(check_sizing.cap() == 1);
        for (int i=0; i<32; i++) {
            check_sizing.append(i);
        }
        assert(check_sizing.cap() == 32);

        for (int i=32; i>7; i--) {
            check_sizing.remove(i);
        }
        assert(check_sizing.cap() == 8);

        vector<int> vec_overload = {1,2,3,4,5,6,7,8};
        ArrayList check_overload(vec_overload);
        assert(check_overload.cap() == 8);
        assert(check_overload.length() == 8);
        for (int i=0; i<vec_overload.size(); i++) {
            assert(vec_overload[i] == check_overload[i]);
        }

        check_overload.insert(f,1);
        check_overload.insert(f,3);
        check_overload.insert(f,7);
        assert(check_overload[1] == f);
        assert(check_overload[3] == f);
        assert(check_overload[7] == f);
    }
}

int main() {
    test_arraylist(5);
    first_n_primes(10);
    return 0;
}
