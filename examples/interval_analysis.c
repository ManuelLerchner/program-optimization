int M[];
int A;

void main(int A0) {
  int i = 0;
  while (i < 42) {
    if (0 <= i && i < 42) {
      int A1 = A + i;
      M[A1] = i;
      i = i + 1;
    }
  }
}