int I;
int R;
int M[];

void main(int A0, int i, int j) {
  int x = M[I];
  int y = 1;

  while (x > 0) {
    y = x * y;
    x = x - 1;
  }

  M[R] = y;
}