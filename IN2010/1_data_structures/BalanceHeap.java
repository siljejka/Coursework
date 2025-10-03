import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.PriorityQueue;


// Class which returns a balanced priority queue
public class BalanceHeap {

  public static void main(String[] args) throws IOException {
      BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
      int[] inputArray = in.lines().mapToInt(i -> Integer.parseInt(i)).toArray();
      int N = inputArray.length;

      PriorityQueue<Integer> minHeap = new PriorityQueue<>();
      for (int i=0; i<N; i++) {
        minHeap.offer(inputArray[i]);
      }

      BalanceHeap heap = new BalanceHeap();
      heap.printRoots(minHeap);
  }

  /* Recursive method which finds the middle element then makes a new
  PriorityQueue from the left and right elements of the middle element, and
  prints the middle element. */
  public void printRoots (PriorityQueue<Integer> arr) {

    PriorityQueue<Integer> left = new PriorityQueue<Integer>();
    PriorityQueue<Integer> right = new PriorityQueue<Integer>();

    if (arr.size() < 1) {
    }
    else {
      int mid = (int)(arr.size()/2);
      for (int i = 0; i < mid; i++) {
        left.offer(arr.poll());
      }
      System.out.println(arr.poll());
      int N = arr.size();
      for (int i = 0; i < N; i++) {
        right.offer(arr.poll());
      }
      printRoots(left);
      printRoots(right);
    }
  }
}
