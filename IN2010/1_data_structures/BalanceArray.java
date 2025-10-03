import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


// Class which returns a balanced array
public class BalanceArray {
  /* Main method */
  public static void main(String[] args) throws IOException {
      BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
      int[] sortedArray = in.lines().mapToInt(i -> Integer.parseInt(i)).toArray();
      int N = sortedArray.length;
      BalanceArray list = new BalanceArray(N, sortedArray);
      list.addRoots(0, N-1);
      for (int i=0; i<N; i++) {
        System.out.println(list.get(i));
      }
  }

  public int counter = 0; // Counts how many recursions there's been of addRoots
  public int len; // Length of the sorted list
  public int[] balancedArray; // Balanced array
  public int[] sortedArray; // Sorted array

  // Constructor
  public BalanceArray (int N, int[] arr) {
    sortedArray = arr;
    balancedArray = new int[N];
    len = N;
  }

  /* Recursive method which groups the array in left and using limits, inputs
  the values in the balancedArray. */
  public void addRoots (int low, int high) {
    if (low > high) {
    }
    else {
      int mid = (int)((low + high) / 2);
      balancedArray[counter] = sortedArray[mid];
      counter += 1;
      addRoots(low, mid-1);
      addRoots(mid+1, high);
    }
  }

  // Returns the value of the element at index i
  public int get (int i){
    return balancedArray[i];
  }

  // Prints a list of balancedArray
  public void printList (int N) {
    System.out.print("[");
    for (int i=0; i<N-1; i++) {
      System.out.print(balancedArray[i]);
      System.out.print(", ");
    }
    System.out.print(balancedArray[N-1]);
    System.out.print("]");
  }
}
