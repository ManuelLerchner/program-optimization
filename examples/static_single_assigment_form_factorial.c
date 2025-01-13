int M[];
int x;
int y;
int i;
int R;

void main() {
  x = M[i];
  y = 1;
  while (x > 1) {
    y = y * x;
    x = x - 1;
  }
  M[R] = y;
}