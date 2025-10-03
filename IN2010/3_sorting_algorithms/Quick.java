class Quick extends Sorter {

    void sort() {
        int[] A = this.A;
        recursion(A, 0, this.n - 1);
    }

    void recursion(int[] A, int low, int high) {
        int index;
        if (low < high) {
            index = partition(A, low, high);
            recursion(A, low, index - 1);
            recursion(A, index + 1, high);
        }
    }

    int partition(int[] A, int low, int high) {
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (lt(A[j], A[high])) {
                i++;
                swap(i, j);
            }
        }
        swap(i+1, high);
        return i+1;
    }

    String algorithmName() {
        return "quick";
    }
}
