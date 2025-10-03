import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


// Class to initate a node
class Node {
  public int val;
  public Node next;
  public Node last;

  public Node(int x) {
    val = x;
  }
}

// Class which creates a oldTeque linked list using nodes
public class oldTeque {
  /* Main method take input in the form of a list with N+1 lines, where the
  first line is the value N and the other lines are in the form: "method int". */
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int N = Integer.parseInt(br.readLine());
    oldTeque list = new oldTeque();

    for (int i = 0; i < N; i++) {
      String[] line = br.readLine().split(" ");
      String cmd = line[0];
      int x = Integer.parseInt(line[1]);
      if (cmd.equals("push_back")) {
        list.push_back(x);
      }
      else if (cmd.equals("push_middle")) {
        list.push_middle(x);
      }
      else if (cmd.equals("push_front")) {
        list.push_front(x);
      }
      else if (cmd.equals("get")) {
        list.get(x);
      }
      else if (cmd.equals("print")) {
        list.print();
      }
    }
  }
  private Node head; // Reference to the first element in the list
  private Node tail; // Reference to the last element in the list
  public int lenList; // Length of the list

  // Constructor, initiates reference Nodes with null and lenList to 0
  public oldTeque() {
    head = null;
    tail = null;
    lenList = 0;
  }

  // Adds element to the back of the queue
  public void push_back(int x) {
    if (lenList == 0) {
      tail = new Node(x);
      head = tail;
    }
    else if (lenList == 1) {
      tail = new Node(x);
      head.next = tail;
      tail.last = head;
    }
    else {
      Node oldTail = tail;
      tail = new Node(x);
      tail.last = oldTail;
      oldTail.next = tail;
    }
    lenList++;
  }

  // Adds element to the middle of the queue
  public void push_middle(int x) {
    if (lenList == 0) {
      head = new Node(x);
      tail = head;
    }
    else if (lenList == 1) {
      head = new Node(x);
      head.next = tail;
      tail.last = head;
    }
    else {
      Node index = head;
      for (int i = 0; i < (lenList+1)/2 -1; i++) {
        index = head.next;
      }
      Node stomach = new Node(x);
      stomach.next = index.next;
      stomach.last = index;
      index.next.last = stomach;
      index.next = stomach;
    }
    lenList++;
  }

  // Adds element to the front of the queue
  public void push_front(int x) {
    if (lenList == 0) {
      head = new Node(x);
      tail = head;
    }
    else if (lenList == 1) {
      head = new Node(x);
      head.next = tail;
      tail.last = head;
    }
    else {
      Node oldHead = head;
      head = new Node(x);
      head.next = oldHead;
      oldHead.last = head;
    }
    lenList++;
  }

  // Method which prints the list
  public void print() {
    Node index = head;
    System.out.print("New list: [");
    for (int i = 0; i < lenList-1; i++){
      System.out.print(index.val);
      System.out.print(", ");
      index = index.next;
    }
    System.out.print(index.val);
    System.out.println("]");
  }

  // Returns the value of the ith element
  public int get(int x) {
    Node index = head;
    for (int i = 0; i < x; i++) {
      index = index.next;
    }
    System.out.println(index.val);
    return index.val;
  }
}
