class Insertion extends Sorter {

    void sort() {
        int[] A = this.A;
        for (int i = 1; i < this.n; i++) {
            int j = i;
            while ((0 < j) && lt(A[j], A[j-1])) {
                swap(j, j-1);
                j--;
            }
        }
    }

    String algorithmName() {
        return "insertion";
    }
}
