class Bubble extends Sorter {

    void sort() {
        int[] A = this.A;
        for (int i = 0; i < this.n - 1; i++) {
            for (int j = 0; j < (n - i - 1); j++) {
                if (lt(A[j+1], A[j])) {
                      swap(j, j+1);
                }
            }
        }
    }

    String algorithmName() {
        return "bubble";
    }
}
