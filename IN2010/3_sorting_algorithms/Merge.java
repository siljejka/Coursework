import java.util.Arrays;

class Merge extends Sorter {

    void sort() {
        int[] A = this.A;
        if (lt(1, n)) {
            recursion(A);
        }
    }

    void recursion(int[] A) {
        if (lt(2, A.length)) {
            int i = (int)(A.length / 2);

            int[] A_1 = Arrays.copyOfRange(A, 0, i);
            int[] A_2 = Arrays.copyOfRange(A, i, A.length);

            recursion(A_1);
            recursion(A_2);
            merge(A, A_1, A_2);
        }
        else if (lt(1, A.length)) {
            if (gt(A[0], A[1])) {
                swaps++;
                int tmp = A[0];
                A[0] = A[1];
                A[1] = tmp;
            }
        }
    }

    void merge(int[] A, int[] A_1, int[] A_2) {
        int i = 0, j = 0;
        while (lt(i, A_1.length) && lt(j, A_2.length)) {
            if (leq(A_1[i], A_2[j])) {
                A[i+j] = A_1[i];
                swaps++;
                i++;
            }
            else {
                A[i+j] = A_2[j];
                swaps++;
                j++;
            }
        }
        while (lt(i, A_1.length)) {
            A[i+j] = A_1[i];
            swaps++;
            i++;
        }
        while (lt(j, A_2.length)) {
            A[i+j] = A_2[j];
            swaps++;
            j++;
        }
    }

    String algorithmName() {
        return "merge";
    }
}
