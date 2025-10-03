import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.LinkedList;

// Class which creates a Teque linked list using nodes
public class Teque {
  /* Main method take input in the form of a list with N+1 lines, where the
  first line is the value N and the other lines are in the form: "method int". */
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int N = Integer.parseInt(br.readLine());
    Teque list = new Teque();

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
        list.getVal(x);
      }
    }
  }
  private LinkedList<Integer> list; // Tailed linked list
  public int lenList; // Length of the list

  // Constructor, initiates reference Nodes with null and lenList to 0
  public Teque() {
    list = new LinkedList<Integer>();
    lenList = 0;
  }

  // Adds element to the back of the queue
  public void push_back(int x) {
    list.add(x);
    lenList++;
  }

  // Adds element to the middle of the queue
  public void push_middle(int x) {
    if (lenList < 2) {
      list.add(x);
    }
    else {
      int index = (int)((lenList+1)/2);
      list.add(index, x);
    }
    lenList++;
  }

  // Adds element to the front of the queue
  public void push_front(int x) {
    list.addFirst(x);
    lenList++;
  }

  // Method which prints the list
  public void printList() {
    System.out.print("New list: [");
    for (int i = 0; i < lenList-1; i++){
      System.out.print(list.get(i));
      System.out.print(", ");
    }
    System.out.print(list.get(lenList-1));
    System.out.println("]");
  }

  // Returns the value of the ith element
  public int getVal(int x) {
    System.out.println(list.get(x));
    return list.get(x);
  }
}
